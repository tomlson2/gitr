import os
import openai

class Model:

    def __init__(self) -> None:
        openai.api_key = self.read_auth()
        self.model = "code-davinci-002"

    def read_auth(self):
        with open('key.txt', 'r') as file:
            auth_key = file.readline().strip()
        return auth_key
    
    def generate_completion(self):
        p = """generate a README.md file for the following code:

    fn send_post(&mut self, path: &str, body: &str) -> Result<String, reqwest::Error> {
        let payload_nonce = format!("nonce={}", &self.nonce.to_string());
        let signature = self.get_signature(path.to_owned(), payload_nonce.to_owned());

        let endpoint = format!("https://api.kraken.com{}", path);

        let headers = self.get_headers(&signature);

        let response = self
            .http
            .post(&endpoint)
            .headers(headers)
            .body(payload_nonce)
            .send()?;

        let text = response.text()?;
        Ok(text)
    }

    fn send_get(&mut self, path: &str) -> Result<String, reqwest::Error> {
        let endpoint = format!("https://api.kraken.com{}", path);

        let response = self.http.get(&endpoint).send()?;

        let text = response.text()?;
        Ok(text)
    }

}


struct TradingData {
    kraken_client: KrakenClient,
    ohlc_data: Option<Vec<Ohlc>>,
    order_book_data: Option<OrderBook>,
    trade_data: Option<Vec<Trade>>,
}

impl TradingData {
    fn new(kraken_client: KrakenClient) -> Self {
        TradingData {
            kraken_client,
            ohlc_data: None,
            order_book_data: None,
            trade_data: None,
        }
    }

    fn get_ohlc_data(&mut self, pair: &str, interval: &str, since: Option<u64>, use_cache: bool) -> Result<(), Box<dyn std::error::Error>> {
        let path = format!("/0/public/OHLC?pair={}&interval={}", pair, interval);

        if use_cache && self.ohlc_data.is_some() {
            return Ok(());
        }
        println!("hello!");

        let response = if let Some(since) = since {
            self.kraken_client.send_get(&format!("{}&since={}", path, since))
        } else {
            self.kraken_client.send_get(&path)
        }?;

        let value: Value = serde_json::from_str(&response)?;
        let prep = &value["result"]["XXBTZUSD"].to_string();
        let data: Vec<Ohlc> = serde_json::from_str(&prep)?;
        self.ohlc_data = Some(data);

        Ok(())
    }

    fn get_order_book_data(
        &mut self,
        pair: &str,
        count: u32,
    ) -> Result<(), Box<dyn std::error::Error>> {
        let path = format!("/0/public/Depth?pair={}&count={}", pair, count);
        let response = self.kraken_client.send_get(&path)?;
        let value: Value = serde_json::from_str(&response)?;
        let prep = &value["result"]["XXBTZUSD"].to_string();
        let data: OrderBook = serde_json::from_str(&prep)?;
        self.order_book_data = Some(data);
        Ok(())
    }

    fn get_trade_data(
        &mut self, 
        pair: &str
    ) -> Result<(), Box<dyn std::error::Error>> {
        let path = format!("/0/public/Trades?pair={}", pair);
        let response = self.kraken_client.send_get(&path)?;
        let value: Value = serde_json::from_str(&response)?;
        let prep = &value["result"]["XXBTZUSD"].to_string();
        let data: Vec<Trade> = serde_json::from_str(&prep)?;
        self.trade_data = Some(data);
        Ok(())
    }
}
        """
        completion = openai.Completion.create(model="text-davinci-003", prompt=p)
        return completion


if __name__ == "__main__":
    print(Model().generate_completion())