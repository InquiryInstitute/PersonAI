"""
Real-time fine-tuning engine for personAI
Enables continuous learning from user interactions while maintaining safety
"""
from typing import List, Dict, Optional
import os
import logging
from datetime import datetime
import json
import torch
from pathlib import Path

logger = logging.getLogger(__name__)


class FineTuningConfig:
    """Configuration for real-time fine-tuning"""
    
    def __init__(self):
        self.enabled = os.getenv("FINETUNING_ENABLED", "false").lower() == "true"
        self.auto_tune = os.getenv("FINETUNING_AUTO", "false").lower() == "true"
        self.learning_rate = float(os.getenv("FINETUNING_LR", "1e-5"))
        self.steps_per_session = int(os.getenv("FINETUNING_STEPS", "100"))
        self.buffer_size = int(os.getenv("FINETUNING_BUFFER_SIZE", "100"))
        self.backend = os.getenv("FINETUNING_BACKEND", "ane")  # ane, cpu, cuda
        self.checkpoint_dir = Path(os.getenv("FINETUNING_CHECKPOINT_DIR", "./checkpoints"))
        self.max_checkpoints = int(os.getenv("FINETUNING_MAX_CHECKPOINTS", "10"))
        
        # Safety controls
        self.require_approval = os.getenv("FINETUNING_REQUIRE_APPROVAL", "true").lower() == "true"
        self.content_filter = os.getenv("FINETUNING_CONTENT_FILTER", "true").lower() == "true"
        self.rollback_enabled = os.getenv("FINETUNING_ROLLBACK", "true").lower() == "true"


class ConversationBuffer:
    """Buffer for storing recent conversations for fine-tuning"""
    
    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self.messages: List[Dict[str, str]] = []
        
    def add_message(self, role: str, content: str, timestamp: Optional[str] = None):
        """Add a message to the buffer"""
        if timestamp is None:
            timestamp = datetime.utcnow().isoformat()
            
        message = {
            "role": role,
            "content": content,
            "timestamp": timestamp
        }
        
        self.messages.append(message)
        
        # Keep buffer size limited
        if len(self.messages) > self.max_size:
            self.messages.pop(0)
    
    def get_training_pairs(self) -> List[Dict[str, str]]:
        """Extract user-assistant pairs for training"""
        pairs = []
        for i in range(len(self.messages) - 1):
            if self.messages[i]["role"] == "user" and self.messages[i + 1]["role"] == "assistant":
                pairs.append({
                    "input": self.messages[i]["content"],
                    "output": self.messages[i + 1]["content"],
                    "timestamp": self.messages[i]["timestamp"]
                })
        return pairs
    
    def clear(self):
        """Clear the buffer"""
        self.messages = []


class FineTuningEngine:
    """Real-time fine-tuning engine with safety controls"""
    
    def __init__(self, config: Optional[FineTuningConfig] = None):
        self.config = config or FineTuningConfig()
        self.buffer = ConversationBuffer(max_size=self.config.buffer_size)
        self.model = None
        self.tokenizer = None
        self.optimizer = None
        self.training_history = []
        
        # Create checkpoint directory
        self.config.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Fine-tuning engine initialized: enabled={self.config.enabled}, backend={self.config.backend}")
    
    def initialize_model(self, model, tokenizer):
        """Initialize the model and optimizer for fine-tuning"""
        self.model = model
        self.tokenizer = tokenizer
        
        if self.config.enabled:
            # Set up optimizer for selected layers
            trainable_params = self._select_trainable_parameters()
            self.optimizer = torch.optim.AdamW(
                trainable_params,
                lr=self.config.learning_rate
            )
            logger.info(f"Model initialized for fine-tuning with {len(list(trainable_params))} trainable parameters")
    
    def _select_trainable_parameters(self):
        """Select specific parameters to fine-tune (e.g., last few layers)"""
        # Fine-tune only last 2 transformer blocks for efficiency
        # This can be adjusted based on model architecture
        trainable = []
        
        # Example for transformer models
        if hasattr(self.model, 'transformer'):
            layers = self.model.transformer.h[-2:]  # Last 2 layers
            for layer in layers:
                trainable.extend(layer.parameters())
        else:
            # Fallback: tune all parameters (not recommended for large models)
            trainable = self.model.parameters()
        
        return trainable
    
    def add_interaction(self, user_input: str, assistant_output: str):
        """Add a user-assistant interaction to the buffer"""
        self.buffer.add_message("user", user_input)
        self.buffer.add_message("assistant", assistant_output)
        
        logger.debug(f"Added interaction to buffer. Buffer size: {len(self.buffer.messages)}")
        
        # Auto-tune if enabled and buffer has enough data
        if self.config.auto_tune and not self.config.require_approval:
            if len(self.buffer.get_training_pairs()) >= 10:
                self.fine_tune_step()
    
    def content_filter_check(self, text: str) -> bool:
        """Check if content is safe for training (basic implementation)"""
        if not self.config.content_filter:
            return True
        
        # Basic content filtering - expand as needed
        unsafe_patterns = [
            "hate speech", "violence", "explicit",
            "harmful", "illegal", "dangerous"
        ]
        
        text_lower = text.lower()
        for pattern in unsafe_patterns:
            if pattern in text_lower:
                logger.warning(f"Content filter blocked text containing: {pattern}")
                return False
        
        return True
    
    def fine_tune_step(self, num_steps: Optional[int] = None) -> Dict[str, float]:
        """Perform fine-tuning steps on buffered data"""
        if not self.config.enabled:
            logger.warning("Fine-tuning is disabled")
            return {"error": "disabled"}
        
        if self.model is None or self.tokenizer is None:
            logger.error("Model not initialized")
            return {"error": "model_not_initialized"}
        
        num_steps = num_steps or self.config.steps_per_session
        training_pairs = self.buffer.get_training_pairs()
        
        if not training_pairs:
            logger.info("No training pairs available")
            return {"error": "no_data"}
        
        # Filter content
        safe_pairs = [
            pair for pair in training_pairs
            if self.content_filter_check(pair["input"]) and self.content_filter_check(pair["output"])
        ]
        
        if not safe_pairs:
            logger.warning("All training pairs filtered out by content filter")
            return {"error": "filtered"}
        
        # Save checkpoint before fine-tuning (for rollback)
        if self.config.rollback_enabled:
            self.save_checkpoint("pre_finetune")
        
        # Perform training steps
        total_loss = 0.0
        start_time = datetime.utcnow()
        
        self.model.train()
        
        for step in range(num_steps):
            # Sample a training pair
            pair = safe_pairs[step % len(safe_pairs)]
            
            # Tokenize
            inputs = self.tokenizer(
                pair["input"],
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            )
            
            labels = self.tokenizer(
                pair["output"],
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            )
            
            # Move to appropriate device
            device = self._get_device()
            inputs = {k: v.to(device) for k, v in inputs.items()}
            labels = labels["input_ids"].to(device)
            
            # Forward pass
            outputs = self.model(**inputs, labels=labels)
            loss = outputs.loss
            
            # Backward pass
            loss.backward()
            self.optimizer.step()
            self.optimizer.zero_grad()
            
            total_loss += loss.item()
        
        self.model.eval()
        
        end_time = datetime.utcnow()
        elapsed = (end_time - start_time).total_seconds()
        
        # Record training history
        history_entry = {
            "timestamp": start_time.isoformat(),
            "steps": num_steps,
            "avg_loss": total_loss / num_steps,
            "elapsed_seconds": elapsed,
            "steps_per_second": num_steps / elapsed if elapsed > 0 else 0,
            "training_pairs": len(safe_pairs)
        }
        
        self.training_history.append(history_entry)
        
        logger.info(
            f"Fine-tuning complete: {num_steps} steps in {elapsed:.2f}s "
            f"({history_entry['steps_per_second']:.1f} steps/s), avg loss: {history_entry['avg_loss']:.4f}"
        )
        
        # Save checkpoint after successful fine-tuning
        self.save_checkpoint("post_finetune")
        
        return history_entry
    
    def _get_device(self) -> str:
        """Determine the appropriate device for training"""
        if self.config.backend == "ane":
            # For Apple Neural Engine - requires special setup
            # This is a placeholder; actual ANE integration requires private APIs
            return "mps" if torch.backends.mps.is_available() else "cpu"
        elif self.config.backend == "cuda":
            return "cuda" if torch.cuda.is_available() else "cpu"
        else:
            return "cpu"
    
    def save_checkpoint(self, name: str):
        """Save model checkpoint for rollback"""
        if not self.config.rollback_enabled:
            return
        
        checkpoint_path = self.config.checkpoint_dir / f"{name}_{datetime.utcnow().isoformat()}.pt"
        
        torch.save({
            "model_state_dict": self.model.state_dict(),
            "optimizer_state_dict": self.optimizer.state_dict() if self.optimizer else None,
            "training_history": self.training_history,
            "timestamp": datetime.utcnow().isoformat()
        }, checkpoint_path)
        
        logger.info(f"Checkpoint saved: {checkpoint_path}")
        
        # Clean up old checkpoints
        self._cleanup_old_checkpoints()
    
    def _cleanup_old_checkpoints(self):
        """Remove old checkpoints beyond max limit"""
        checkpoints = sorted(
            self.config.checkpoint_dir.glob("*.pt"),
            key=lambda p: p.stat().st_mtime
        )
        
        if len(checkpoints) > self.config.max_checkpoints:
            for old_checkpoint in checkpoints[:-self.config.max_checkpoints]:
                old_checkpoint.unlink()
                logger.debug(f"Removed old checkpoint: {old_checkpoint}")
    
    def rollback(self, checkpoint_name: Optional[str] = None):
        """Rollback to a previous checkpoint"""
        if not self.config.rollback_enabled:
            logger.warning("Rollback is disabled")
            return False
        
        if checkpoint_name:
            checkpoint_path = self.config.checkpoint_dir / f"{checkpoint_name}.pt"
        else:
            # Get most recent checkpoint
            checkpoints = sorted(
                self.config.checkpoint_dir.glob("*.pt"),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            )
            if not checkpoints:
                logger.error("No checkpoints available for rollback")
                return False
            checkpoint_path = checkpoints[0]
        
        if not checkpoint_path.exists():
            logger.error(f"Checkpoint not found: {checkpoint_path}")
            return False
        
        # Load checkpoint
        checkpoint = torch.load(checkpoint_path)
        self.model.load_state_dict(checkpoint["model_state_dict"])
        
        if self.optimizer and checkpoint.get("optimizer_state_dict"):
            self.optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
        
        logger.info(f"Rolled back to checkpoint: {checkpoint_path}")
        return True
    
    def get_training_stats(self) -> Dict:
        """Get statistics about fine-tuning"""
        if not self.training_history:
            return {"total_steps": 0, "sessions": 0}
        
        total_steps = sum(h["steps"] for h in self.training_history)
        avg_steps_per_sec = sum(h["steps_per_second"] for h in self.training_history) / len(self.training_history)
        avg_loss = sum(h["avg_loss"] for h in self.training_history) / len(self.training_history)
        
        return {
            "total_steps": total_steps,
            "sessions": len(self.training_history),
            "avg_steps_per_second": avg_steps_per_sec,
            "avg_loss": avg_loss,
            "latest_session": self.training_history[-1] if self.training_history else None
        }
    
    def export_training_log(self, filepath: str):
        """Export training history to JSON"""
        with open(filepath, 'w') as f:
            json.dump({
                "config": vars(self.config),
                "training_history": self.training_history,
                "stats": self.get_training_stats()
            }, f, indent=2)
        
        logger.info(f"Training log exported to {filepath}")
