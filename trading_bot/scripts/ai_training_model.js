const tf = require('@tensorflow/tfjs-node');
const fs = require('fs');
const csv = require('csv-parser');

async function loadData(filePath) {
    const data = [];
    const labels = [];
    
    return new Promise((resolve, reject) => {
        fs.createReadStream(filePath)
            .pipe(csv())
            .on('data', (row) => {
                data.push([parseFloat(row.open), parseFloat(row.high), parseFloat(row.low), parseFloat(row.close), parseFloat(row.volume)]);
                labels.push(parseFloat(row.close));
            })
            .on('end', () => {
                console.log('CSV file successfully processed');
                resolve({ data, labels });
            })
            .on('error', reject);
    });
}

function preprocessData(data, labels) {
    const xs = tf.tensor2d(data);
    const ys = tf.tensor1d(labels);
    return { xs, ys };
}

async function trainModel(xs, ys) {
    const model = tf.sequential();
    model.add(tf.layers.dense({ units: 50, inputShape: [5], activation: 'relu' }));
    model.add(tf.layers.dense({ units: 1 }));

    model.compile({ optimizer: 'adam', loss: 'meanSquaredError' });

    await model.fit(xs, ys, {
        epochs: 100,
        shuffle: true,
        validationSplit: 0.2,
    });

    return model;
}

async function main() {
    const { data, labels } = await loadData('../data/historical_data.csv');
    const { xs, ys } = preprocessData(data, labels);

    const model = await trainModel(xs, ys);
    await model.save('file://../models/trained_trading_model');
}

main();