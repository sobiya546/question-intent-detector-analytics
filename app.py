from flask import Flask, render_template, request, jsonify
import pickle

app = Flask(__name__)


# ============================================================
# LOAD MODEL
# ============================================================

with open("model.pkl", "rb") as file:
    saved_model = pickle.load(file)

model = saved_model["model"]
mlb = saved_model["mlb"]


# ============================================================
# INTENT ACTIONS
# ============================================================

actions = {

    "Definition":
        "Provide a simple definition and key points.",

    "Explanation":
        "Provide a step-by-step explanation.",

    "Example":
        "Provide a practical example.",

    "Problem Solving":
        "Provide the solution with clear steps.",

    "Revision":
        "Provide short revision notes and important points.",

    "Comparison":
        "Provide a comparison showing the main differences."
}


# ============================================================
# SUBJECT + TOPIC DETECTION
# ============================================================

def detect_subject_topic(question):

    q = question.lower()


    # ========================================================
    # DBMS
    # ========================================================

    if "normalization" in q:
        return "DBMS", "Normalization"

    if (
        "primary key" in q
        or "foreign key" in q
        or "candidate key" in q
        or "super key" in q
    ):
        return "DBMS", "Keys"

    if "index" in q or "indexing" in q:
        return "DBMS", "Indexes"

    if (
        "transaction" in q
        or "acid" in q
        or "commit" in q
        or "rollback" in q
    ):
        return "DBMS", "Transactions"

    if "dbms" in q or "database" in q:
        return "DBMS", "DBMS Basics"


    # ========================================================
    # COMPUTER NETWORKS
    # ========================================================

    if "tcp" in q and "udp" in q:
        return "Computer Networks", "TCP vs UDP"

    if "http" in q and "https" in q:
        return "Computer Networks", "HTTP vs HTTPS"

    if "lan" in q and "wan" in q:
        return "Computer Networks", "LAN vs WAN"

    if "tcp" in q:
        return "Computer Networks", "TCP"

    if "udp" in q:
        return "Computer Networks", "UDP"

    if "osi" in q:
        return "Computer Networks", "OSI Model"

    if "https" in q:
        return "Computer Networks", "HTTPS"

    if "http" in q:
        return "Computer Networks", "HTTP"

    if "lan" in q:
        return "Computer Networks", "LAN"

    if "wan" in q:
        return "Computer Networks", "WAN"

    if "network" in q:
        return "Computer Networks", "Networking Basics"


    # ========================================================
    # JAVA
    # ========================================================

    if "polymorphism" in q:
        return "Java", "Polymorphism"

    if "inheritance" in q:
        return "Java", "Inheritance"

    if "encapsulation" in q:
        return "Java", "Encapsulation"

    if "abstraction" in q:
        return "Java", "Abstraction"

    if "class" in q and "object" in q:
        return "Java", "Class and Object"

    if "oop" in q or "object oriented" in q:
        return "Java", "OOP"

    if "java" in q:
        return "Java", "Java Basics"


    # ========================================================
    # C PROGRAMMING
    # ========================================================

    if "pointer" in q:
        return "C Programming", "Pointers"

    if "factorial" in q:
        return "C Programming", "Factorial"

    if "loop" in q and (
        " c " in " " + q + " "
        or "c program" in q
        or "c programming" in q
    ):
        return "C Programming", "Loops"

    if "data type" in q and (
        " c " in " " + q + " "
        or "c program" in q
        or "c programming" in q
    ):
        return "C Programming", "Variables and Data Types"

    if "variable" in q and (
        " c " in " " + q + " "
        or "c program" in q
        or "c programming" in q
    ):
        return "C Programming", "Variables and Data Types"

    if "program output" in q:
        return "C Programming", "Program Output"

    if "c programming" in q or "c program" in q:
        return "C Programming", "C Basics"


    # ========================================================
    # DATA STRUCTURES
    # ========================================================

    if "array" in q and "linked list" in q:
        return "Data Structures", "Array vs Linked List"

    if "stack" in q and "queue" in q:
        return "Data Structures", "Stack vs Queue"

    if "tree" in q:
        return "Data Structures", "Trees"

    if "graph" in q or "shortest path" in q:
        return "Data Structures", "Graphs"

    if "recursion" in q:
        return "Data Structures", "Recursion"

    if (
        "binary search" in q
        or "linear search" in q
        or "searching" in q
    ):
        return "Data Structures", "Searching"

    if (
        "sorting" in q
        or "bubble sort" in q
        or "merge sort" in q
    ):
        return "Data Structures", "Sorting"

    if "linked list" in q:
        return "Data Structures", "Linked List"

    if "array" in q:
        return "Data Structures", "Arrays"

    if "stack" in q:
        return "Data Structures", "Stack"

    if "queue" in q:
        return "Data Structures", "Queue"

    if "data structure" in q:
        return "Data Structures", "Data Structures Basics"


    # ========================================================
    # SQL
    # ========================================================

    if "join" in q:
        return "SQL", "Joins"

    if "subquery" in q or "sub query" in q:
        return "SQL", "Subqueries"

    if "string function" in q:
        return "SQL", "String Functions"

    if "group by" in q:
        return "SQL", "GROUP BY"

    if "having" in q:
        return "SQL", "HAVING"

    if "select" in q and "sql" in q:
        return "SQL", "SELECT"

    if "where" in q and "sql" in q:
        return "SQL", "WHERE"

    if "sql" in q:
        return "SQL", "SQL Basics"


    # ========================================================
    # MATHEMATICS
    # ========================================================

    if (
        "profit" in q
        or "loss" in q
        or "gain" in q
        or "selling price" in q
        or "cost price" in q
    ):
        return "Mathematics", "Profit and Loss"

    if "ratio" in q or "proportion" in q:
        return "Mathematics", "Ratio and Proportion"

    if "percentage" in q or "percent" in q:
        return "Mathematics", "Percentage"

    if "compound interest" in q:
        return "Mathematics", "Compound Interest"

    if "simple interest" in q:
        return "Mathematics", "Simple Interest"

    if "average" in q or "mean" in q:
        return "Mathematics", "Average"

    if "probability" in q:
        return "Mathematics", "Probability"

    if "quadratic" in q:
        return "Mathematics", "Quadratic Equations"

    if "equation" in q or "value of x" in q:
        return "Mathematics", "Algebra"


    # ========================================================
    # PYTHON
    # ========================================================

    if "python" in q:

        if "dictionary" in q or "dictionaries" in q:
            return "Python", "Dictionaries"

        if "list" in q:
            return "Python", "Lists"

        if "function" in q:
            return "Python", "Functions"

        if "loop" in q:
            return "Python", "Loops"

        if "condition" in q:
            return "Python", "Conditions"

        if "variable" in q:
            return "Python", "Variables"

        return "Python", "Python Basics"


    # ========================================================
    # DEFAULT
    # ========================================================

    return "General", "General"


# ============================================================
# RULE-BASED INTENT DETECTION
# ============================================================

def detect_intents_from_words(question):

    q = question.lower()

    detected = []


    # --------------------------------------------------------
    # DEFINITION
    # --------------------------------------------------------

    definition_phrases = [
        "what is",
        "what are",
        "define",
        "meaning of",
        "tell me about"
    ]

    for phrase in definition_phrases:

        if phrase in q:
            detected.append("Definition")
            break


    # --------------------------------------------------------
    # EXPLANATION
    # --------------------------------------------------------

    explanation_phrases = [
        "explain",
        "explain how",
        "how does",
        "how do",
        "teach me",
        "teach it",
        "describe",
        "why is",
        "why are",
        "how it works",
        "how it work",
        "don't understand",
        "do not understand"
    ]

    for phrase in explanation_phrases:

        if phrase in q:
            detected.append("Explanation")
            break


    # --------------------------------------------------------
    # EXAMPLE
    # --------------------------------------------------------

    example_phrases = [
        "example",
        "examples",
        "demonstrate",
        "show me",
        "show an example",
        "sample",
        "with code",
        "using code",
        "code example",
        "real world"
    ]

    for phrase in example_phrases:

        if phrase in q:
            detected.append("Example")
            break


    # --------------------------------------------------------
    # COMPARISON
    # --------------------------------------------------------

    comparison_phrases = [
        "compare",
        "comparison",
        "difference",
        "differences",
        "different from",
        "contrast",
        "versus",
        " vs ",
        "which is better"
    ]

    for phrase in comparison_phrases:

        if phrase in q:
            detected.append("Comparison")
            break


    # --------------------------------------------------------
    # PROBLEM SOLVING
    # --------------------------------------------------------

    problem_phrases = [
        "solve",
        "calculate",
        "find the answer",
        "work out",
        "solve this",
        "calculate this",
        "solution"
    ]

    for phrase in problem_phrases:

        if phrase in q:
            detected.append("Problem Solving")
            break


    # --------------------------------------------------------
    # REVISION
    # --------------------------------------------------------

    revision_phrases = [
        "revision",
        "revise",
        "revision notes",
        "revision points",
        "important points",
        "quick notes",
        "short notes",
        "exam notes",
        "exam revision"
    ]

    for phrase in revision_phrases:

        if phrase in q:
            detected.append("Revision")
            break


    return detected


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return render_template("index.html")


# ============================================================
# CLASSIFY QUESTION
# ============================================================

@app.route("/classify", methods=["POST"])
def classify():

    data = request.get_json()

    question = data.get("question", "").strip()


    # --------------------------------------------------------
    # EMPTY QUESTION
    # --------------------------------------------------------

    if not question:

        return jsonify({
            "error": "Please enter a question."
        })


    # ========================================================
    # MACHINE LEARNING PREDICTION
    # ========================================================

    probabilities = model.predict_proba([question])[0]


    # Threshold
    threshold = 0.20


    ml_intents = []


    for intent, probability in zip(
        mlb.classes_,
        probabilities
    ):

        if probability >= threshold:

            ml_intents.append(intent)


    # ========================================================
    # RULE-BASED INTENT DETECTION
    # ========================================================

    rule_intents = detect_intents_from_words(question)


    # ========================================================
    # COMBINE ML + RULE RESULTS
    # ========================================================

    final_intents = []


    # First add ML predictions

    for intent in ml_intents:

        if intent not in final_intents:

            final_intents.append(intent)


    # Then add rule predictions

    for intent in rule_intents:

        if intent not in final_intents:

            final_intents.append(intent)


    # ========================================================
    # FALLBACK
    # ========================================================

    if len(final_intents) == 0:

        best_index = probabilities.argmax()

        final_intents = [
            mlb.classes_[best_index]
        ]


    # ========================================================
    # KEEP INTENTS IN FIXED ORDER
    # ========================================================

    intent_order = [
        "Definition",
        "Explanation",
        "Example",
        "Problem Solving",
        "Revision",
        "Comparison"
    ]


    ordered_intents = []


    for intent in intent_order:

        if intent in final_intents:

            ordered_intents.append(intent)


    # ========================================================
    # SUBJECT + TOPIC
    # ========================================================

    subject, topic = detect_subject_topic(question)


    # ========================================================
    # RECOMMENDED ACTIONS
    # ========================================================

    recommended_actions = []


    for intent in ordered_intents:

        if intent in actions:

            recommended_actions.append(
                actions[intent]
            )


    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    return jsonify({

        "intents": ordered_intents,

        "subject": subject,

        "topic": topic,

        "actions": recommended_actions

    })


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )