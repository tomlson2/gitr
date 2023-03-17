import fetch from 'node-fetch';

async function getData() {
    const res = await fetch('http://localhost:5000/api/data');
    const data = await res.json();
    return data;
}