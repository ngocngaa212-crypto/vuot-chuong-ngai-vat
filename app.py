import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Oggy Rượt Đuổi Gián - Subway Surfers Style", layout="centered"
)

st.title("🏃‍♂️ Game: Gián Chạy Trốn Mèo Oggy!")
st.write(
    "Bạn là chú gián tinh ranh! Dùng phím **Mũi tên Trái / Phải** hoặc **A / D** để đổi 3 làn đường, né bẫy và đừng để mèo Oggy 3D tóm gọn nhé!"
)

game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            background: #111;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Comic Sans MS', cursive, sans-serif;
            color: white;
            overflow: hidden;
        }
        #gameContainer {
            position: relative;
            text-align: center;
        }
        #gameCanvas {
            border: 4px solid #3498db;
            background: #1e272e;
            box-shadow: 0 0 30px rgba(52, 152, 219, 0.6);
            display: block;
        }
        #restartBtn {
            display: none;
            position: absolute;
            top: 55%;
            left: 50%;
            transform: translate(-50%, -50%);
            padding: 14px 30px;
            font-size: 20px;
            background-color: #e74c3c;
            color: white;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            font-weight: bold;
            box-shadow: 0 6px 15px rgba(0,0,0,0.6);
            z-index: 10;
        }
        #restartBtn:hover {
            background-color: #c0392b;
        }
    </style>
</head>
<body>

    <div id="gameContainer">
        <canvas id="gameCanvas" width="450" height="600"></canvas>
        <button id="restartBtn" onclick="resetGame()">Chơi Lại Ngay!</button>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const restartBtn = document.getElementById("restartBtn");

        // 3 làn đường (Trái, Giữa, Phải)
        const lanes = [110, 225, 340];

        // Nhân vật Gián (Bạn)
        let player = {
            laneIndex: 1,
            y: 450,
            width: 45,
            height: 45,
            targetX: 225,
            x: 225
        };

        // Kẻ đuổi bắt phía sau: Mèo Oggy (dùng ảnh model 3D chuẩn hoạt hình)
        const oggyPursuer = {
            x: 225,
            y: 510,
            width: 70,
            height: 70
        };

        let obstacles = [];
        let score = 0;
        let gameOver = false;
        let frameCount = 0;
        let gameSpeed = 5;

        // Tải hình ảnh sprites từ nguồn chuẩn
        const roachImg = new Image();
        roachImg.src = 'https://cdn-icons-png.flaticon.com/512/3468/3468377.png'; // Chú gián

        const oggyImg = new Image();
        oggyImg.src = 'https://cdn-icons-png.flaticon.com/512/616/616430.png'; // Mèo Oggy đuổi theo sau

        const trapImg = new Image();
        trapImg.src = 'https://cdn-icons-png.flaticon.com/512/2936/2936735.png'; // Bẫy / chướng ngại vật trong nhà

        // Điều khiển phím
        document.addEventListener("keydown", (e) => {
            if (gameOver) return;
            if (e.key === "ArrowLeft" || e.key === "a" || e.key === "A") {
                if (player.laneIndex > 0) player.laneIndex--;
            }
            if (e.key === "ArrowRight" || e.key === "d" || e.key === "D") {
                if (player.laneIndex < 2) player.laneIndex++;
            }
        });

        function spawnObstacle() {
            let randomLane = Math.floor(Math.random() * 3);
            obstacles.push({
                laneIndex: randomLane,
                y: -60,
                width: 50,
                height: 50,
                speed: gameSpeed
            });
        }

        function update() {
            if (gameOver) return;

            // Di chuyển làn mượt mà
            player.targetX = lanes[player.laneIndex];
            player.x += (player.targetX - player.x) * 0.25;

            // Mèo Oggy chạy bám theo vị trí X của gián với độ trễ mượt
            oggyPursuer.x += (player.x - oggyPursuer.x) * 0.1;

            // Tăng tốc độ theo điểm
            gameSpeed = 5 + Math.floor(score / 8) * 0.5;

            frameCount++;
            if (frameCount % 45 === 0) {
                spawnObstacle();
            }

            for (let i = 0; i < obstacles.length; i++) {
                let obs = obstacles[i];
                obs.y += obs.speed;

                // Kiểm tra va chạm với chướng ngại vật
                let obsX = lanes[obs.laneIndex];
                if (
                    obs.laneIndex === player.laneIndex &&
                    player.y < obs.y + obs.height - 10 &&
                    player.y + player.height > obs.y + 10
                ) {
                    gameOver = true;
                    restartBtn.style.display = "block";
                }

                // Vượt qua chướng ngại vật thành công
                if (obs.y > canvas.height) {
                    obstacles.splice(i, 1);
                    score += 1;
                    i--;
                }
            }
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 1. Vẽ nền sàn nhà / căn bếp phối cảnh 3D
            ctx.fillStyle = "#2d3436";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Vùng đường chạy chính giữa
            ctx.fillStyle = "#636e72";
            ctx.beginPath();
            ctx.moveTo(140, 0); ctx.lineTo(310, 0); ctx.lineTo(410, canvas.height); ctx.lineTo(40, canvas.height);
            ctx.fill();

            // Vạch phân làn đường chạy
            ctx.strokeStyle = "#ffeaa7";
            ctx.lineWidth = 3;
            ctx.setLineDash([15, 15]);
            ctx.beginPath(); ctx.moveTo(200, 0); ctx.lineTo(170, canvas.height); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(250, 0); ctx.lineTo(280, canvas.height); ctx.stroke();
            ctx.setLineDash([]);

            // 2. Vẽ Chướng ngại vật
            for (let obs of obstacles) {
                let drawX = lanes[obs.laneIndex] - obs.width / 2;
                ctx.drawImage(trapImg, drawX, obs.y, obs.width, obs.height);
            }

            // 3. Vẽ Nhân vật Chú Gián (chạy phía trước)
            ctx.drawImage(roachImg, player.x - player.width / 2, player.y, player.width, player.height);

            // 4. Vẽ Mèo Oggy đuổi theo sát nút ngay phía sau lưng gián!
            ctx.drawImage(oggyImg, oggyPursuer.x - oggyPursuer.width / 2, oggyPursuer.y, oggyPursuer.width, oggyPursuer.height);

            // 5. Hiển thị Điểm số
            ctx.fillStyle = "#ffeaa7";
            ctx.font = "bold 22px 'Comic Sans MS'";
            ctx.fillText("ĐIỂM TRỐN CHẠY: " + score, 20, 35);

            // 6. Màn hình Game Over
            if (gameOver) {
                ctx.fillStyle = "rgba(0, 0, 0, 0.85)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                ctx.fillStyle = "#ff7675";
                ctx.font = "bold 28px 'Comic Sans MS'";
                ctx.textAlign = "center";
                ctx.fillText("ÔI KHÔNG! OGGY ĐÃ TÓM ĐƯỢC BẠN!", canvas.width / 2, canvas.height / 2 - 40);

                ctx.fillStyle = "white";
                ctx.font = "20px 'Comic Sans MS'";
                ctx.fillText("Tổng điểm trốn chạy: " + score, canvas.width / 2, canvas.height / 2 + 10);
                ctx.textAlign = "left";
            }
        }

        function gameLoop() {
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }

        function resetGame() {
            player.laneIndex = 1;
            player.x = lanes[1];
            oggyPursuer.x = lanes[1];
            obstacles = [];
            score = 0;
            gameSpeed = 5;
            gameOver = false;
            restartBtn.style.display = "none";
        }

        gameLoop();
    </script>
</body>
</html>
"""

components.html(game_html, height=620)
