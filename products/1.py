import pandas as pd

# Create a sample DataFrame with the required columns
data = {
    "username": ["user1", "user2", "user3"],
    "email": ["user1@gmail.com", "user2@gmail.com", "user3@gmail.com"],
    "password": ["password1", "password2", "password3"]
}

df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv("users.csv", index=False)
