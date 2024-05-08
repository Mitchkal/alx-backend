const express = require('express');
const redis = require('redis');
const { get } = require('request');
const { promisify } = require('util');

const client = redis.createClient();
client.on('connect', () => {
  console.log('Redis client connected to the server');
});
client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

const app = express();
const Port = 1245;

const listProducts = [
  { id: 1, name: 'Suitcase 250', price: 50, stock: 4 },
  { id: 2, name: 'Suitcase 450', price: 100, stock: 10 },
  { id: 3, name: 'Suitcase 650', price: 350, stock: 2 },
  { id: 4, name: 'Suitcase 1050', price: 550, stock: 5 },
];

function getItemById(id) {
  return listProducts.find((item) => item.id === id);
}

const reserveStockById = (itemId, stock) => {
  client.set(`item.${itemId}`, stock, redis.print);
};

const getCurrentReservedStockById = async (itemId) => {
  const getAsync = promisify(client.get).bind(client);
  return await getAsync(`item.${itemId}`);
};

app.get('/list_products', (_req, res) => {
  res.json(
    listProducts.map(({ id, name, price, stock }) => ({
      itemId: id,
      itemName: name,
      price,
      initialAvailableQuantity: stock,
    })),
  );
});

app.get('/list_products/:itemId', async (req, res) => {
  const { itemId } = req.params;
  const product = getItemById(parseInt(itemId));

  if (!product) {
    return res.json({ status: 'Product not found' });
  }
  const currentQuantity = await getCurrentReservedStockById(itemId);
  res.json({
    itemId: product.id,
    itemName: product.name,
    price: product.price,
    initialAvailableQuantity: product.stock,
    currentQuantity: currentQuantity || 0,
  });
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const { itemId } = req.params;
  const product = getItemById(parseInt(itemId));
  console.log(`product is ${product}`);

  if (!product) {
    return res.json({ status: 'Product not found' });
  }
  const currentQuantity = await getCurrentReservedStockById(itemId);
  const availableStock = product.stock - (currentQuantity || 0);

  if (availableStock <= 0) {
    return res.json({
      status: 'Not enough stock available',
      itemId: product.id,
    });
  }
  reserveStockById(itemId, currentQuantity ? currentQuantity + 1 : 1);

  res.json({ status: 'Reservation confirmed', itemId: product.id });
});

app.listen(Port, (error) => {
  if (!error) {
    console.log(`Server running at localhost:${Port}/`);
  } else {
    console.log('Error occured, server cannot start', error);
  }
});
