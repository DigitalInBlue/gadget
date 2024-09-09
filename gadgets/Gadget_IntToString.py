from GadgetComponent import GadgetComponent
import hashlib
import random

class Gadget_IntToString(GadgetComponent):
    def run(self, input_data: int) -> str:
        if not isinstance(input_data, int):
            self.logger.error(f"Invalid input type for {self.get_name()}: Expected int, got {type(input_data)}")
            return None

        self.logger.info(f"{self.get_name()} received: {input_data}")

        # Step 1: Hash the integer using SHA-256
        hash_object = hashlib.sha256(str(input_data).encode())
        hex_digest = hash_object.hexdigest()

        # Step 2: Add some randomness to ensure the output isn't predictable
        random.seed(input_data)
        random_suffix = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))

        # Step 3: Convert the first few characters of the hash to a new string and mix with the random suffix
        output_data = f"{hex_digest[:10]}-{random_suffix}"

        self.logger.info(f"{self.get_name()} produced: {output_data}")
        return output_data
    
    def get_name(self) -> str:
        return 'Numerical Symbolic Disassociation Engine'
