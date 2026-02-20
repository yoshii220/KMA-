// チャットアプリケーションのメインJavaScript

const API_BASE_URL = '/api';

// DOM要素
const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const sendButton = document.getElementById('sendButton');
const suggestionsButtons = document.getElementById('suggestionsButtons');
const updateButton = document.getElementById('updateButton');
const loading = document.getElementById('loading');

// 初期化
document.addEventListener('DOMContentLoaded', () => {
    loadSuggestions();
    setupEventListeners();
    checkStatus();
});

// イベントリスナーの設定
function setupEventListeners() {
    sendButton.addEventListener('click', sendMessage);
    
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    chatInput.addEventListener('input', autoResize);

    updateButton.addEventListener('click', triggerUpdate);
}

// テキストエリアの自動リサイズ
function autoResize() {
    chatInput.style.height = 'auto';
    chatInput.style.height = Math.min(chatInput.scrollHeight, 150) + 'px';
}

// サジェスト質問を読み込む
async function loadSuggestions() {
    try {
        const response = await fetch(`${API_BASE_URL}/suggestions`);
        const data = await response.json();
        
        if (data.suggestions) {
            displaySuggestions(data.suggestions);
        }
    } catch (error) {
        console.error('Error loading suggestions:', error);
    }
}

// サジェスト質問を表示
function displaySuggestions(suggestions) {
    suggestionsButtons.innerHTML = '';
    
    suggestions.forEach(suggestion => {
        const button = document.createElement('button');
        button.className = 'suggestion-button';
        button.textContent = suggestion;
        button.addEventListener('click', () => {
            chatInput.value = suggestion;
            sendMessage();
        });
        suggestionsButtons.appendChild(button);
    });
}

// メッセージを送信
async function sendMessage() {
    const question = chatInput.value.trim();
    
    if (!question) return;

    // ユーザーメッセージを表示
    addMessage(question, 'user');
    
    // 入力欄をクリア
    chatInput.value = '';
    chatInput.style.height = 'auto';
    
    // 送信ボタンを無効化
    sendButton.disabled = true;
    
    // ローディング表示
    showLoading(true);

    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question }),
        });

        const data = await response.json();
        
        if (response.ok) {
            // ボットの回答を表示
            addMessage(data.answer, 'bot', data.sources);
        } else {
            addMessage('申し訳ございません。エラーが発生しました。', 'bot');
        }
    } catch (error) {
        console.error('Error sending message:', error);
        addMessage('申し訳ございません。通信エラーが発生しました。', 'bot');
    } finally {
        showLoading(false);
        sendButton.disabled = false;
        chatInput.focus();
    }
}

// メッセージを追加
function addMessage(text, type, sources = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    // テキストを段落に分割
    const paragraphs = text.split('\n').filter(p => p.trim());
    paragraphs.forEach(para => {
        const p = document.createElement('p');
        p.textContent = para;
        contentDiv.appendChild(p);
    });
    
    // ソース情報を追加（ボットメッセージの場合）
    if (type === 'bot' && sources && sources.length > 0) {
        const sourcesDiv = document.createElement('div');
        sourcesDiv.className = 'sources';
        
        const sourcesTitle = document.createElement('p');
        sourcesTitle.className = 'sources-title';
        sourcesTitle.textContent = '📚 参考情報:';
        sourcesDiv.appendChild(sourcesTitle);
        
        sources.forEach(source => {
            const sourceItem = document.createElement('div');
            sourceItem.className = 'source-item';
            
            const categorySpan = document.createElement('span');
            categorySpan.className = 'source-category';
            categorySpan.textContent = source.category || 'カテゴリ';
            
            const link = document.createElement('a');
            link.href = source.url;
            link.target = '_blank';
            link.textContent = source.title;
            
            sourceItem.appendChild(categorySpan);
            sourceItem.appendChild(link);
            
            sourcesDiv.appendChild(sourceItem);
        });
        
        contentDiv.appendChild(sourcesDiv);
    }
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // スクロールを最下部へ
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// ローディング表示の切り替え
function showLoading(show) {
    loading.style.display = show ? 'flex' : 'none';
}

// ステータスチェック
async function checkStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/status`);
        const data = await response.json();
        
        if (!data.chatbot_ready) {
            addMessage('システムの初期化中です。少々お待ちください...', 'bot');
        }
    } catch (error) {
        console.error('Error checking status:', error);
    }
}

// データ更新をトリガー
async function triggerUpdate() {
    if (!confirm('データを更新しますか？この処理には数分かかる場合があります。')) {
        return;
    }

    updateButton.disabled = true;
    updateButton.textContent = '更新中...';
    showLoading(true);

    try {
        const response = await fetch(`${API_BASE_URL}/update`, {
            method: 'POST',
        });

        const data = await response.json();
        
        if (response.ok) {
            alert('データの更新が完了しました！');
            addMessage('データが更新されました。最新の情報で回答できます。', 'bot');
        } else {
            alert('更新中にエラーが発生しました。');
        }
    } catch (error) {
        console.error('Error triggering update:', error);
        alert('通信エラーが発生しました。');
    } finally {
        showLoading(false);
        updateButton.disabled = false;
        updateButton.textContent = '🔄 データを更新';
    }
}
