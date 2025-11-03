from context import Keyregistry, Context
def create_user_a_context():
  try:
    # creating keys
    user_name_key = Keyregistry.register("UserName", str)
    user_age_key = Keyregistry.register("UserAge", int)

    #creating context
    ctx = Context()
    ctx.set(user_name_key, "artur")
    ctx.set(user_age_key, 21)

    print("[PROJECT A]")
    print(ctx.get(user_name_key))  
    print(ctx.get(user_age_key))
    return ctx 
  except ValueError as e:
    print("error: ", e) 
    return None