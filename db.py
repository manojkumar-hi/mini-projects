from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB connection - ADD YOUR PASSWORD
client = AsyncIOMotorClient("mongodb+srv://manoj:1234@cluster0.mktow4w.mongodb.net/admin?appName=Cluster0&retryWrites=true&loadBalanced=false&replicaSet=atlas-w7idog-shard-0&readPreference=primary&srvServiceName=mongodb&connectTimeoutMS=10000&w=majority&authSource=admin&authMechanism=SCRAM-SHA-1")
db = client["studenthub"] # Replace 'studenthub' with your database name
