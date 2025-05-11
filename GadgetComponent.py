import hashlib
import time
import logging
from datetime import datetime
from PIL import Image

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Base class for all Gadget components
class GadgetComponent:
    previous_block = None  # The previous block in the chain

    def __init__(self):
        self.logger = logger
        self.timestamp = datetime.now()
        self.run_time = None
        self.mint_time = None
        self.nonce = 0
        self.previous_hash = None
        self.block_hash = None
        self.value = None

    def get_name(self):
        """Return the name of the component"""
        return self.__class__.__name__

    def run(self, input_data):
        """Process the input and return the output.
        Each subclass will implement this method.
        """
        raise NotImplementedError("Subclasses must implement the 'run' method.")

    def execute(self, input_data, previous_block=None):
        """Wrapper for running the component's logic and validating the output."""
        previous_block = previous_block or GadgetComponent.previous_block

        start_time = time.time()
        self.value = self.run(input_data)
        self.run_time = time.time() - start_time

        if not self.is_valid_output(self.value):
            self.logger.error(
                f"{self.get_name()} returned an invalid output type: {type(self.value)}"
            )
            return None

        # Mint a block after successful execution
        start_time = time.time()
        self._mint_block()
        self.mint_time = time.time() - start_time
        return self.value

    def is_valid_output(self, output):
        """Ensure the output type is one of the valid types"""
        return isinstance(
            output, (int, float, str, bool, Image.Image, dict)
        )  # dict used for JSON

    def get_blockchain(self):
        """Get the blockchain starting from the current block"""
        current_block = self
        blockchain = []
        while current_block:
            blockchain.append(current_block)
            current_block = current_block.previous_block
        return blockchain

    def get_blockchain_hashes(self):
        """Get the blockchain hashes starting from the current block"""
        return [block.block_hash for block in self.get_blockchain()]

    def get_blockchain_details(self):
        """Get the blockchain details starting from the current block"""
        return [
            (block.get_name(), block.timestamp, block.previous_hash, block.block_hash)
            for block in self.get_blockchain()
        ]

    def get_blockchain_summary(self):
        """Get a summary of the blockchain starting from the current block"""
        return f"Blockchain Summary: {self.get_name()} -> " + " -> ".join(
            [block.get_name() for block in self.get_blockchain()][1:]
        )

    def get_blockchain_hashes_summary(self):
        """Get a summary of the blockchain hashes starting from the current block"""
        return f"Blockchain Hashes: {self.get_name()} -> " + " -> ".join(
            [block.block_hash for block in self.get_blockchain()][1:]
        )

    def get_block_hash(self):
        """Get the current block's hash"""
        return self.block_hash

    def get_previous_hash(self):
        """Get the previous block's hash"""
        return self.previous_hash

    def get_block_timestamp(self):
        """Get the current block's timestamp"""
        return self.timestamp

    def get_value(self):
        """Get the value of the current block"""
        return self.value

    def get_nonce(self):
        """Get the nonce of the current block"""
        return self.nonce

    def _mint_block(self, difficulty=5):
        """Mint a new block for the blockchain based on the component's execution with proof of work."""
        self.logger.info(f'Starting minting process for "{self.get_name()}"...')
        self.nonce = 0  # Initialize the nonce

        # Get the previous block's hash (if any)
        if GadgetComponent.previous_block:
            self.previous_hash = GadgetComponent.previous_block.block_hash

        # Proof of work: keep adjusting the nonce until we find a valid hash
        target = "0" * difficulty  # The hash must have 'difficulty' leading zeros
        while True:
            # Combine execution details to create block data with the nonce
            block_data = f"{self.get_name()}-{self.value}-{self.timestamp}-{self.run_time}-{self.previous_hash}-{self.nonce}"
            self.block_hash = hashlib.sha256(block_data.encode()).hexdigest()

            # Check if the block hash meets the difficulty target
            if self.block_hash[:difficulty] == target:
                break

            # Increment nonce for the next iteration
            self.nonce += 1

        # Log block details
        if self.previous_hash is None:
            self.logger.info(
                f'Genesis block minted for "{self.get_name()}" - Hash: {self.block_hash[:8]} (Nonce: {self.nonce})'
            )
        else:
            self.logger.info(
                f'Minted block for "{self.get_name()}" - Hash: {self.block_hash[:8]}, Previous Hash: {self.previous_hash[:8]} (Nonce: {self.nonce})'
            )

        # Set this block as the previous block for the next component
        GadgetComponent.previous_block = self

    @staticmethod
    def valid_input_output_types():
        """List of valid input/output types"""
        return (int, float, str, bool, Image.Image, dict)  # dict used for JSON data
