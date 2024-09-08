import os
import importlib
import inspect
import pytest
from GadgetComponent import GadgetComponent

# Discover all Python files except the test and base Gadget files
component_files = [f[:-3] for f in os.listdir() if f.endswith(".py") and f not in ["Gadget.py", "GadgetComponent.py", "test_gadget_components.py"]]


# Parameterize the tests by dynamically loading all the component files
@pytest.mark.parametrize("module_name", component_files)
def test_component_validity(module_name):
    """
    Test that each component module contains valid GadgetComponent classes.
    The test checks if:
    - The class is a subclass of GadgetComponent.
    - The class implements `getName()` and `run()`.
    - The `run()` method works with valid input/output types.
    """
    # Dynamically import the module
    module = importlib.import_module(module_name)

    # Find all classes in the module
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if issubclass(obj, GadgetComponent) and obj != GadgetComponent:
            # Instantiate the component
            component_instance = obj()

            # Test if the component has getName() and run() methods
            assert hasattr(component_instance, 'getName'), f"{name} does not implement getName()"
            assert hasattr(component_instance, 'run'), f"{name} does not implement run()"

            # Test getName()
            component_name = component_instance.getName()
            assert isinstance(component_name, str), f"{name}.getName() should return a string"

            # Get the valid input and output types
            valid_types = component_instance.valid_input_output_types()
            assert isinstance(valid_types, tuple), f"{name}.valid_input_output_types() should return a tuple of types"

            # Test run() method with valid inputs
            run_signature = inspect.signature(component_instance.run)
            expected_input_type = run_signature.parameters['input_data'].annotation

            for input_type in valid_types:
                # Generate a valid input based on the type
                valid_input = generate_valid_input(input_type)
                assert valid_input is not None, f"Could not generate a valid input for type {input_type}"

                # Run the component with the input
                output = component_instance.run(valid_input)

                if input_type == expected_input_type:
                    # If the input type matches the expected input type, check for a valid output
                    assert any(isinstance(output, valid_type) for valid_type in valid_types), (
                        f"{name}.run() should return a valid output type, got {type(output)}"
                    )
                else:
                    # If the input type does not match, we expect None or a valid output type
                    assert output is None or any(isinstance(output, valid_type) for valid_type in valid_types), (
                        f"{name}.run() should return None or a valid output type for invalid input, got {output}"
                    )


# Parameterize the tests by dynamically loading all the component files
@pytest.mark.parametrize("module_name", component_files)
def test_component_run_annotations(module_name):
    """
    Test that each component module contains valid GadgetComponent classes.
    The test checks if:
    - The class is a subclass of GadgetComponent.
    - The class implements `getName()` and `run()`.
    - The `run()` method works with valid input/output types.
    """
    # Dynamically import the module
    module = importlib.import_module(module_name)

    # Find all classes in the module
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if issubclass(obj, GadgetComponent) and obj != GadgetComponent:
            # Instantiate the component
            component_instance = obj()

            # Test if the component has getName() and run() methods
            assert hasattr(component_instance, 'getName'), f"{name} does not implement getName()"
            assert hasattr(component_instance, 'run'), f"{name} does not implement run()"

            # Test getName()
            component_name = component_instance.getName()
            assert isinstance(component_name, str), f"{name}.getName() should return a string"

            # Test that there are type annotations on the run function
            # Get the signature of the `run` method
            signature = inspect.signature(GadgetComponent.run)

            # Check the input_data annotation
            input_data_annotation = signature.parameters['input_data'].annotation
            assert input_data_annotation is not None, f"Expected 'input_data' type have a type annotation, but got {input_data_annotation}"

            # Check the return type annotation
            return_annotation = signature.return_annotation
            assert return_annotation is not None, f"Expected return type to have a type annotation, but got {return_annotation}"


def generate_valid_input(input_type):
    """
    Generate valid input based on the required input type.
    Handles int, float, str, bool, Image, and JSON (dict).
    """
    import random
    from PIL import Image

    if input_type == int:
        return random.randint(1, 100)
    elif input_type == float:
        return random.uniform(1.0, 100.0)
    elif input_type == str:
        return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10))
    elif input_type == bool:
        return random.choice([True, False])
    elif input_type == Image.Image:
        return Image.new('RGB', (64, 64), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    elif input_type == dict:
        return {"key": "value", "number": random.randint(1, 100)}
    return None
