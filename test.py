class Example:
    def __init__(self, *args, **kwargs):
        print("Pozycyjne argumenty (*args):", args)
        print("Argumenty nazwane (**kwargs):", kwargs)

# Przykładowe użycie
example = Example(1, 2, 3, name="John", age=30)