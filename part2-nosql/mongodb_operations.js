/**
 * FlexiMart MongoDB Operations - Dataset Optimized Version
 * Collection: products
 */

// --- Operation 1: Load Data ---
// Logic to insert the provided high-diversity JSON catalog
const productCatalog = [ /* Insert the full JSON array provided in your prompt here */ ];

db.products.drop(); 
db.products.insertMany(productCatalog);

// --- Operation 2: Basic Query ---
// Business Question: Find all Electronics under 50,000 INR.
// Note: This will return Sony Headphones and OnePlus Nord based on your data.
print("--- Operation 2: Electronics priced < 50,000 ---");
const basicQuery = db.products.find(
    { 
        category: "Electronics", 
        price: { $lt: 50000 } 
    },
    { name: 1, price: 1, stock: 1, _id: 0 }
).toArray();
printjson(basicQuery);

// --- Operation 3: Review Analysis ---
// Business Question: Products with average rating >= 4.0.
// Uses the 'reviews' array to calculate averages across the diverse catalog.
print("--- Operation 3: Average Product Ratings (>= 4.0) ---");
const reviewAnalysis = db.products.aggregate([
    { $unwind: "$reviews" },
    {
        $group: {
            _id: "$name",
            averageRating: { $avg: "$reviews.rating" },
            totalReviews: { $sum: 1 }
        }
    },
    { $match: { averageRating: { $gte: 4.0 } } },
    { $project: { _id: 1, averageRating: { $round: ["$averageRating", 1] }, totalReviews: 1 } }
]).toArray();
printjson(reviewAnalysis);

// --- Operation 4: Update Operation ---
// Business Question: Add a new review to product "ELEC001" (Galaxy S21 Ultra).
print("--- Operation 4: Adding new review to ELEC001 ---");
db.products.updateOne(
    { product_id: "ELEC001" },
    { 
        $push: { 
            reviews: {
                user_id: "U999",
                username: "NewReviewer",
                rating: 4,
                comment: "Good value after software updates.",
                date: new Date().toISOString().split('T')[0] // Formats as YYYY-MM-DD
            } 
        } 
    }
);

// --- Operation 5: Complex Aggregation ---
// Business Question: Category performance (Avg Price, Product Count).
// Sorted by average price descending.
print("--- Operation 5: Category Performance Report ---");
const categorySummary = db.products.aggregate([
    {
        $group: {
            _id: "$category",
            avg_price: { $avg: "$price" },
            product_count: { $sum: 1 },
            total_stock: { $sum: "$stock" }
        }
    },
    {
        $project: {
            category: "$_id",
            avg_price: { $round: ["$avg_price", 2] },
            product_count: 1,
            total_stock: 1,
            _id: 0
        }
    },
    { $sort: { avg_price: -1 } }
]).toArray();
printjson(categorySummary);