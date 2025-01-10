import express from "express"
import mongoose from "mongoose"
import dotenv from "dotenv"

dotenv.config()

const app = express()

app.use(express.json())
app.use(express.urlencoded({ extended: true }))

mongoose.connect(process.env.MONGODB_URI)
  .then(() => console.log('Connected to MongoDB successfully'))
  .catch((err) => console.error('MongoDB connection error:', err))

app.get('/', (req, res) => {
  res.json({ message: 'Welcome to the API' })
})

const PORT = process.env.PORT || 5000
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`)
})