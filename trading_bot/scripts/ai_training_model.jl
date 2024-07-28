# Load required packages
using CSV
using DataFrames
using ScikitLearn
using ScikitLearn: fit!, predict, train_test_split, accuracy_score
using Random

# Load the data
function load_data(file_path::String)
    return CSV.read(file_path, DataFrame)
end

# Preprocess the data
function preprocess_data(df::DataFrame)
    df = dropmissing(df)
    label = ifelse.(df.close[2:end] .> df.close[1:end-1], 1, 0)
    X = select!(df[1:end-1], Not(:label))
    X.label = label
    return X[!, Not(:label)], label
end

# Train the model
function train_model(X, y)
    model = @sk_import ensemble:RandomForestClassifier
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = model()
    fit!(clf, X_train, y_train)
    
    y_pred_train = predict(clf, X_train)
    y_pred_test = predict(clf, X_test)
    
    println("Training Accuracy: ", accuracy_score(y_train, y_pred_train))
    println("Test Accuracy: ", accuracy_score(y_test, y_pred_test))
    
    return clf
end

# Save the trained model
function save_model(model, file_name::String)
    ScikitLearnBase.save(file_name, model)
    println("Model saved to $file_name")
end

# Main function
function main()
    data = load_data("../data/historical_data.csv")
    if size(data, 1) == 0
        println("No data loaded. Exiting.")
        return
    end
    
    X, y = preprocess_data(data)
    model = train_model(X, y)
    save_model(model, "../models/trained_trading_model.pkl")
end

main()