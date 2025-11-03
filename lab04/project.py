from client_a import create_user_a_context
from client_b import create_user_b_context
from context import Context, Keyregistry

ctx1 = create_user_a_context()
ctx2 = create_user_b_context()