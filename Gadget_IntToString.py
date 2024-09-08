from GadgetComponent import GadgetComponent


class Gadget_IntToString(GadgetComponent):
    def run(self, input_data: int) -> str:
        if not isinstance(input_data, int):
            self.logger.error(f"Invalid input type for {self.getName()}: Expected int, got {type(input_data)}")
            return None

        self.logger.info(f"{self.getName()} received: {input_data}")
        output_data = str(input_data)  # Convert integer to string
        self.logger.info(f"{self.getName()} produced: {output_data}")
        return output_data

