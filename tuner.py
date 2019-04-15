import os

from hyperparameter_tuner.run_command_generator import run_command_generator as cmd_generator
from hyperparameter_tuner.single_parameter_generator import single_parameter_generator as sgen
from datetime import datetime
import time


def extract_to_csv(path):
    print(path)
    directory = os.fsencode(path)
    output_file = open(f"{path}/summarise.csv", "w+")

    for file in os.listdir(directory):
        filename = os.fsdecode(file)

        if not filename.endswith(".csv"):
            input_file = open(f"{path}/{filename}", "r")
            lines = input_file.readlines()
            output_file.write(f"file:{filename};result:{lines[-2]}")
            print(f"file:{filename};result:{lines[-2]}")
            input_file.close()
    output_file.close()


if __name__ == '__main__':
    output_path = f"hyperparameter_tuner/results/{str(datetime.now()).replace(' ', '')}"
    vgg_16_BP_tuner = cmd_generator([sgen("name", ["resnet"]),
                                             sgen("batch_size", [256, 128, 64]),
                                             sgen("learning_rate", [0.03, 0.01, 0.07, 0.005]),
                                             sgen("learning_type", ["BP", "DFA", "FA"]),
                                             sgen("seed", [10])
                                             ], command_prefix="python experiment.py",
                                            output_path=output_path).run_commands()

    os.system(f"mkdir {output_path}")
    os.system(f"touch {output_path}/summarise.csv")

    for command in vgg_16_BP_tuner:
        print(command)
        os.system(command)
        os.system(f"rm {output_path}/summarise.csv")

        extract_to_csv(output_path)
        print("\n\n\n")
        time.sleep(10)
