def hello_world(my_name: str = 'anonymous') -> str:
    """Say hello to anyone in the world.

    Args:
        my_name (str): Someone's name

    Returns:
        str: A greeting message for someone
    """
    s = f'hello {my_name}'
    print(s)
    return s
