package main

import (
    "encoding/csv"
    "fmt"
    "log"
    "os"

    "gonum.org/v1/gonum/floats"
    "gonum.org/v1/gonum/mat"
    "github.com/sjwhitworth/golearn/base"
    "github.com/sjwhitworth/golearn/evaluation"
    "github.com/sjwhitworth/golearn/knn"
    "github.com/sjwhitworth/golearn/trees"
)

func loadCSV(filename string) *base.DenseInstances {
    file, err := os.Open(filename)
    if err != nil {
        log.Fatal(err)
    }
    defer file.Close()

    reader := csv.NewReader(file)
    records, err := reader.ReadAll()
    if err != nil {
        log.Fatal(err)
    }

    numAttributes := len(records[0])
    attributes := make([]base.Attribute, numAttributes)
    for i := range attributes {
        attributes[i] = base.NewFloatAttribute(fmt.Sprintf("attr_%d", i))
    }

    data := base.NewDenseInstances()
    data.AddAttributes(attributes)
    data.Extend(records)

    return data
}

func main() {
    // Load and preprocess data
    data := loadCSV("../data/historical_data.csv")
    trainData, testData := base.InstancesTrainTestSplit(data, 0.80)

    // Train classifier
    rf := trees.NewRandomForest(100, 3)
    err := rf.Fit(trainData)
    if err != nil {
        log.Fatal(err)
    }

    // Predict test data
    predictions, err := rf.Predict(testData)
    if err != nil {
        log.Fatal(err)
    }

    // Evaluate performance
    confMatrix, err := evaluation.GetConfusionMatrix(testData, predictions)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println(evaluation.GetSummary(confMatrix))
    
    // Saving model (pseudo-code)
    // You can implement model saving with serialization libraries if needed
}