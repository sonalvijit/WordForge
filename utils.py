from server import load_existing_data

def initial_db_state():
     a = load_existing_data()
     print(a[1])

initial_db_state()