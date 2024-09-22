from GadgetComponent import GadgetComponent


class Gadget_StringToBool(GadgetComponent):


    def run(self, input_data: str) -> bool:
        if not isinstance(input_data, str):
            self.logger.error(f"Invalid input type for {self.get_name()}: Expected str, got {type(input_data)}")
            return None

        self.logger.info(f"{self.get_name()} received: {input_data}")
        # Let's define true/false based on specific string values
        output_data = input_data.lower() in ("true", "yes", "1")
        self.logger.info(f"{self.get_name()} produced: {output_data}")
        return output_data


    def get_name(self) -> str:
        return __file__ + ": " + 'Cognitive String Truth Evaluator'
