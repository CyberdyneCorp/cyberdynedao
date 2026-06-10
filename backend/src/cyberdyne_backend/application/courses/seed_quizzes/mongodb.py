from __future__ import annotations

from cyberdyne_backend.application.courses.seed_types import CourseQuiz, opt, q

QUIZ = CourseQuiz(
    per_lesson={
        "The document model": (
            q(
                "How does MongoDB store the documents it groups into collections?",
                (
                    opt("As fixed-schema rows in tables"),
                    opt("As JSON-like documents stored as BSON", correct=True),
                    opt("As plain CSV records"),
                    opt("As key-value pairs only, with no nesting"),
                ),
                "MongoDB is a NoSQL database that stores JSON-like documents, which are stored as BSON.",
            ),
            q(
                "In the relational-to-MongoDB mapping, what does a MongoDB collection correspond to?",
                (
                    opt("A column"),
                    opt("A row"),
                    opt("A table", correct=True),
                    opt("An index"),
                ),
                "The lesson maps a relational table to a MongoDB collection, a row to a document, and a column to a field.",
            ),
            q(
                "What unique value does every MongoDB document get?",
                (
                    opt("A _id", correct=True),
                    opt("A primary key column named id"),
                    opt("A sequential row number"),
                    opt("A collection name"),
                ),
                "Every document gets a unique _id field.",
            ),
        ),
        "CRUD & query operators": (
            q(
                "Which mongosh method reads and returns a single matching document?",
                (
                    opt("find"),
                    opt("findOne", correct=True),
                    opt("insertOne"),
                    opt("updateOne"),
                ),
                "db.users.findOne returns one matching document, while find returns the full set of matches.",
            ),
            q(
                "Which operator does the lesson use to match documents where age is greater than 30?",
                (
                    opt("$gte"),
                    opt("$in"),
                    opt("$gt", correct=True),
                    opt("$ne"),
                ),
                "The query db.users.find({ age: { $gt: 30 } }) uses $gt for greater than.",
            ),
            q(
                "How does the lesson query a nested field such as the city inside address?",
                (
                    opt("By using the dotted path address.city", correct=True),
                    opt("By using a $lookup stage"),
                    opt("By using $exists on address"),
                    opt("By passing address as an array index"),
                ),
                'Nested fields are queried with a dotted path, as in find({ "address.city": "London" }).',
            ),
        ),
        "Aggregation & indexes": (
            q(
                "In the aggregation pipeline, how are documents processed?",
                (
                    opt("All at once with no ordering"),
                    opt(
                        "Through stages that each transform the stream, like Unix pipes",
                        correct=True,
                    ),
                    opt("By a single SQL query translated internally"),
                    opt("Only after an index is built"),
                ),
                "Documents flow through stages, each transforming the stream, similar to Unix pipes.",
            ),
            q(
                "Which aggregation stage groups documents and sums a value per group in the example?",
                (
                    opt("$match"),
                    opt("$group", correct=True),
                    opt("$sort"),
                    opt("$limit"),
                ),
                "The $group stage groups by userId and sums amount into total.",
            ),
            q(
                "What happens to a query when there is no index on the field being filtered?",
                (
                    opt("It scans every document in the collection", correct=True),
                    opt("It returns an error"),
                    opt("It silently returns no results"),
                    opt("It automatically creates a unique index"),
                ),
                "Without an index a query scans every document, whereas an index lets MongoDB jump straight to matches.",
            ),
        ),
    },
    final=(
        q(
            "What is the MongoDB equivalent of a relational JOIN according to the lesson?",
            (
                opt("A foreign key constraint"),
                opt("Embedding documents or using $lookup", correct=True),
                opt("A $match stage"),
                opt("Creating a unique index"),
            ),
            "Related data is handled by embedding documents in one document or by using the $lookup stage.",
        ),
        q(
            "Which mongosh call updates the age field of the user named Ada to 37?",
            (
                opt('db.users.insertOne({ name: "Ada", age: 37 })'),
                opt('db.users.updateOne({ name: "Ada" }, { $set: { age: 37 } })', correct=True),
                opt('db.users.find({ name: "Ada", age: 37 })'),
                opt('db.users.deleteOne({ name: "Ada" })'),
            ),
            "updateOne with a $set operator changes Ada's age to 37.",
        ),
        q(
            "How do you create a unique index on the email field?",
            (
                opt("db.users.createIndex({ email: 1 }, { unique: true })", correct=True),
                opt("db.users.find({ email: { $exists: true } })"),
                opt('db.users.aggregate([{ $group: { _id: "$email" } }])'),
                opt("db.users.updateOne({ email: 1 }, { unique: true })"),
            ),
            "createIndex with the option { unique: true } builds a unique index on email.",
        ),
        q(
            "Which set of operators does the lesson say covers most queries?",
            (
                opt("$match, $group, $sort, $project"),
                opt("$gt/$gte/$lt/$lte, $in, $ne, $exists, $and/$or", correct=True),
                opt("$set, $unset, $inc, $push"),
                opt("$lookup, $limit, $sum, $sort"),
            ),
            "The comparison and logical operators $gt/$gte/$lt/$lte, $in, $ne, $exists, and $and/$or cover most queries.",
        ),
        q(
            "Why can related data in MongoDB often live together in one document?",
            (
                opt("Because collections enforce a fixed schema"),
                opt("Because documents can nest objects and arrays", correct=True),
                opt("Because every field must be indexed"),
                opt("Because BSON forbids references between documents"),
            ),
            "Documents can nest objects and arrays, so related data often lives together instead of being split across tables.",
        ),
    ),
)
