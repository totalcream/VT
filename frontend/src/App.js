import React, { useState } from 'react';
import './App.css';

// 사용자가 제공한 예시 프롬프트를 상수로 정의
const defaultPrompt = `It has been 2399 minute since you started trading.
…
Below, we are providing you with a variety of state data, price data, and predictive signals so you can discover alpha. Below that is your current account information, value, performance, positions, etc.
**ALL OF THE PRICE OR SIGNAL DATA BELOW IS ORDERED: OLDEST → NEWEST**
**Timeframes note:** Unless stated otherwise in a section title, intraday series are provided at **3‑minute intervals**. If a coin uses a different interval, it is explicitly stated in that coin’s section.
---
### CURRENT MARKET STATE FOR ALL COINS
### ALL BTC DATA
current_price = 107982.5, current_ema20 = 107776.85, current_macd = 116.567, current_rsi (7 period) = 62.558
In addition, here is the latest BTC open interest and funding rate for perps (the instrument you are trading):
Open Interest: Latest: 25458.85  Average: 25461.32
Funding Rate: 8.2948e-06
**Intraday series (by minute, oldest → latest):**
Mid prices: [107726.5, 107741.0, 107859.0, 107891.0, 107946.5, 108108.0, 108002.5, 107921.0, 107902.0, 107982.5]
EMA indicators (20‑period): [107540.298, 107556.175, 107584.92, 107617.975, 107644.644, 107695.726, 107721.561, 107740.651, 107755.255, 107776.85]
MACD indicators: [10.802, 21.816, 42.242, 63.667, 77.015, 109.171, 116.049, 116.525, 113.337, 116.567]
RSI indicators (7‑Period): [73.026, 71.971, 81.425, 84.429, 77.695, 87.43, 63.124, 59.094, 56.477, 62.558]
RSI indicators (14‑Period): [59.393, 59.004, 66.193, 69.057, 66.279, 75.216, 61.864, 59.473, 57.972, 61.28]
**Longer‑term context (4‑hour timeframe):**
20‑Period EMA: 107854.332 vs. 50‑Period EMA: 110571.164
3‑Period ATR: 557.797 vs. 14‑Period ATR: 1145.893
Current Volume: 5.495 vs. Average Volume: 5047.135
MACD indicators: [-1914.209, -1853.793, -1799.213, -1697.737, -1610.053, -1515.907, -1413.862, -1316.523, -1263.15, -1126.368]
RSI indicators (14‑Period): [35.766, 37.705, 37.145, 39.797, 39.275, 39.815, 40.696, 40.804, 38.556, 45.44]
---
(XRP, ETH, SOL, BNB, DOGE 데이터... 생략)
---
### HERE IS YOUR ACCOUNT INFORMATION & PERFORMANCE
Current Total Return (percent): 2.59%
Available Cash: 8308.94
**Current Account Value:** 10258.87
Current live positions & performance:
{'symbol': 'XRP', 'quantity': 5164.0, 'entry_price': 2.3, 'current_price': 2.39865, 'liquidation_price': 2.07, 'unrealized_pnl': 493.42, 'leverage': 8, 'exit_plan': {'profit_target': 2.6485, 'stop_loss': 2.1877, 'invalidation_condition': 'BTC breaks below 105,000, confirming deeper market correction'}, 'confidence': 0.62, 'risk_usd': 594.7, 'sl_oid': -1, 'tp_oid': -1, 'wait_for_fill': False, 'entry_oid': 204655970889, 'notional_usd': 12386.63}
Sharpe Ratio: 0.018
`;

const modelOptions = [
    "google/gemma-3-27b-it",
    "openai/gpt-oss-120b",
    "Qwen/Qwen3-30B-A3B-Thinking-2507-FP8",
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B"
];

function App() {
    // State for the user data prompt text area
    const [prompt, setPrompt] = useState(defaultPrompt);
    // State for the selected LLM model from the dropdown
    const [selectedModel, setSelectedModel] = useState("openai/gpt-oss-120b");
    // State to manage the loading status while waiting for the API response
    const [isLoading, setIsLoading] = useState(false);
    // State to store the response from the LLM API
    const [llmResponse, setLlmResponse] = useState('');

    /**
     * Handles the form submission when the "Send to LLM" button is clicked.
     * It sets the loading state, sends the request to the backend API,
     * and updates the response state with the result or an error message.
     */
    const handleSubmit = async () => {
        setIsLoading(true);
        setLlmResponse('');

        try {
            const response = await fetch('/api/llm/trade-decision', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_data_prompt: prompt,
                    model_name: selectedModel,
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'An unknown error occurred');
            }

            const data = await response.json();
            // 수신된 JSON 데이터를 예쁘게 포맷팅하여 표시
            setLlmResponse(JSON.stringify(data, null, 2));

        } catch (error) {
            setLlmResponse(`Error: ${error.message}`);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="App">
            <header className="App-header">
                <h1>LLM Trading Decision Interface</h1>
            </header>
            <main className="main-container">
                <div className="input-section">
                    <h2>Input</h2>
                    <div className="form-group">
                        <label htmlFor="model-select">Select Model:</label>
                        <select
                            id="model-select"
                            value={selectedModel}
                            onChange={(e) => setSelectedModel(e.target.value)}
                        >
                            {modelOptions.map(model => (
                                <option key={model} value={model}>{model}</option>
                            ))}
                        </select>
                    </div>
                    <div className="form-group">
                        <label htmlFor="prompt-textarea">User Data Prompt:</label>
                        <textarea
                            id="prompt-textarea"
                            value={prompt}
                            onChange={(e) => setPrompt(e.target.value)}
                            rows={20}
                        />
                    </div>
                    <button onClick={handleSubmit} disabled={isLoading}>
                        {isLoading ? '수신 중...' : 'LLM에 보내기'}
                    </button>
                </div>
                <div className="output-section">
                    <h2>Output</h2>
                    <textarea
                        readOnly
                        value={isLoading ? '수신 중...' : llmResponse}
                        rows={20}
                        placeholder="Response from LLM will be displayed here..."
                    />
                </div>
            </main>
        </div>
    );
}

export default App;