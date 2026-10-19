import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Oggy & Những Chú Gián: Chạy Trốn", layout="centered"
)

st.title("🪳 Game: Gián Né Mèo Oggy!")
st.write(
    "Bạn là **chú gián** siêu tốc, hãy dùng phím **Mũi tên Trái / Phải** hoặc **A / D** để né Mèo Oggy và nhặt đồ ăn vặt nhé!"
)

game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            background: #1a1a1a;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Comic Sans MS', cursive, sans-serif;
            color: white;
        }
        #gameCanvas {
            border: 4px solid #ffcc00;
            background: #2b2b2b;
            box-shadow: 0 0 25px rgba(255, 204, 0, 0.4);
        }
        #restartBtn {
            display: none;
            position: absolute;
            top: 60%;
            padding: 12px 28px;
            font-size: 18px;
            background-color: #ff4757;
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-weight: bold;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        }
        #restartBtn:hover {
            background-color: #ff6b81;
        }
    </style>
</head>
<body>

    <canvas id="gameCanvas" width="400" height="500"></canvas>
    <button id="restartBtn" onclick="resetGame()">Chơi Lại Nào!</button>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const restartBtn = document.getElementById("restartBtn");

        // Hình ảnh nhân vật (Icon minh họa dễ thương)
        const roachImg = new Image();
        roachImg.src = 'https://cdn-icons-png.flaticon.com/512/2821/2821808.png'; // Biểu tượng chú gián/bọ

        const oggyImg = new Image();
        oggyImg.src = 'https://cdn-icons-png.flaticon.com/512/616/616430.png'; // Biểu tượng mèo

        // Nhân vật chính: Chú Gián
        const player = {
            x: 180,
            y: 420,
            width: 40,
            height: 40,
            speed: 8
        };

        let obstacles = [];
        let score = 0;
        let gameOver = false;
        let frameCount = 0;

        const keys = { left: false, right: false };
        document.addEventListener("keydown", (e) => {
            if (e.key === "ArrowLeft" || e.key === "a" || e.key === "A") keys.left = true;
            if (e.key === "ArrowRight" || e.key === "d" || e.key === "D") keys.right = true;
        });
        document.addEventListener("keyup", (e) => {
            if (e.key === "ArrowLeft" || e.key === "a" || e.key === "A") keys.left = false;
            if (e.key === "ArrowRight" || e.key === "d" || e.key === "D") keys.right = false;
        });

        function spawnOggyObstacle() {
            const size = 45;
            const x = Math.random() * (canvas.width - size);
            obstacles.push({
                x: x,
                y: -50,
                width: size,
                height: size,
                speed: 4 + Math.floor(score / 4) // Tốc độ Mèo Oggy tăng dần theo điểm
            });
        }

        function update() {
            if (gameOver) return;

            // Di chuyển gián
            if (keys.left && player.x > 0) player.x -= player.speed;
            if (keys.right && player.x + player.width < canvas.width) player.x += player.speed;

            // Xuất hiện chướng ngại vật (Mèo Oggy lao xuống)
            frameCount++;
            if (frameCount % 40 === 0) spawnOggyObstacle();

            for (let i = 0; i < obstacles.length; i++) {
                let obs = obstacles[i];
                obs.y += obs.speed;

                // Kiểm tra va chạm (Gián đụng Mèo Oggy là thua)
                if (
                    player.x < obs.x + obs.width - 8 &&
                    player.x + player.width - 8 > obs.x &&
                    player.y < obs.y + obs.height - 8 &&
                    player.y + player.height - 8 > obs.y
                ) {
                    gameOver = true;
                    restartBtn.style.display = "block";
                }

                // Né thành công -> cộng điểm
                if (obs.y > canvas.height) {
                    obstacles.splice(i, 1);
                    score += 1;
                    i--;
                }
            }
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Vẽ sàn bếp (vạch kẻ sọc trang trí)
            ctx.strokeStyle = '#383838';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(133, 0); ctx.lineTo(133, canvas.height);
            ctx.moveTo(266, 0); ctx.lineTo(266, canvas.height);
            ctx.stroke();

            // Vẽ nhân vật (Gián)
            ctx.drawImage(roachImg, player.x, player.y, player.width, player.height);

            // Vẽ chướng ngại vật (Mèo Oggy)
            for (let obs of obstacles) {
                ctx.drawImage(oggyImg, obs.x, obs.y, obs.width, obs.height);
            }

            // Hiển thị điểm số
            ctx.fillStyle = "#ffcc00";
            ctx.font = "bold 22px 'Comic Sans MS', cursive";
            ctx.fillText("Điểm Né Mèo: " + score, 15, 35);

            // Giao diện Game Over
            if (gameOver) {
                ctx.fillStyle = "rgba(0, 0, 0, 0.8)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                ctx.fillStyle = "#ff4757";
                ctx.font = "bold 28px 'Comic Sans MS', cursive";
                ctx.textAlign = "center";
                ctx.fillText("ÔI KHÔNG! BẠN ĐÃ BỊ OGGY TÓM!", canvas.width / 2, canvas.height / 2 - 30);

                ctx.fillStyle = "white";
                ctx.font = "20px 'Comic Sans MS', cursive";
                ctx.fillText("Tổng điểm trốn chạy: " + score, canvas.width / 2, canvas.height / 2 + 15);
            }
        }

        function gameLoop() {
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }

        function resetGame() {
            player.x = 180;
            obstacles = [];
            score = 0;
            gameOver = false;
            frameCount = 0;
            restartBtn.style.display = "none";
        }

        gameLoop();
    </script>
</body>
</html>
"""

components.html(game_html, height=530)
