from core.kernel import Kernel

kernel = Kernel()

while True:
    user_input = input("> ")
    result = kernel.step(user_input)
    print(result)
