import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Oggy 3D Runner - Streamlit Game", layout="centered"
)

st.title("🎮 3D Game: Gián Chạy Trốn Mèo Oggy")
st.write(
    "Dùng phím **Mũi tên Trái / Phải** hoặc **A / D** để di chuyển né chướng ngại vật trên đường đua 3D!"
)

game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            background: #000;
            overflow: hidden;
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        #game-container {
            position: relative;
            width: 700px;
            height: 500px;
            box-shadow: 0 0 25px rgba(255, 165, 0, 0.5);
            border: 4px solid #ffaa00;
        }
        #ui {
            position: absolute;
            top: 15px;
            left: 15px;
            color: white;
            font-size: 22px;
            font-weight: bold;
            text-shadow: 2px 2px 4px #000;
            z-index: 10;
        }
        #gameOverScreen {
            display: none;
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.85);
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: white;
            z-index: 20;
        }
        #gameOverScreen h1 {
            color: #ff4757;
            font-size: 36px;
            margin-bottom: 10px;
        }
        #restartBtn {
            padding: 12px 28px;
            font-size: 18px;
            background-color: #2ed573;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            margin-top: 15px;
        }
        #restartBtn:hover {
            background-color: #26af5f;
        }
    </style>
    <!-- Nhúng thư viện đồ họa 3D Three.js từ CDN -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

    <div id="game-container">
        <div id="ui">Điểm: <span id="scoreVal">0</span></div>
        <div id="gameOverScreen">
            <h1>ÔI KHÔNG! BỊ OGGY TÓM RỒI!</h1>
            <p>Tổng điểm: <span id="finalScore">0</span></p>
            <button id="restartBtn" onclick="restartGame()">Chơi Lại</button>
        </div>
    </div>

    <script>
        let scene, camera, renderer;
        let player, oggy;
        let obstacles = [];
        let score = 0;
        let gameOver = false;
        let gameSpeed = 0.3;
        let lanePositions = [-2.5, 0, 2.5];
        let currentLane = 1; // 0: Trái, 1: Giữa, 2: Phải

        const container = document.getElementById('game-container');

        function init() {
            // 1. Tạo Scene 3D
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x87ceeb); // Màu bầu trời xanh ngắt
            scene.fog = new THREE.FogExp2(0x87ceeb, 0.03);

            // 2. Camera (Góc nhìn phía sau nhân vật giống hình mẫu)
            camera = new THREE.PerspectiveCamera(60, container.clientWidth / container.clientHeight, 0.1, 1000);
            camera.position.set(0, 4, 7);
            camera.lookAt(0, 1, -3);

            // 3. Renderer
            renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(container.clientWidth, container.clientHeight);
            container.appendChild(renderer.domElement);

            // 4. Ánh sáng
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
            scene.add(ambientLight);

            const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
            dirLight.position.set(10, 20, 10);
            scene.add(dirLight);

            // 5. Tạo đường đua màu vàng rực rỡ (giống hình mẫu bạn gửi)
            const roadGeo = new THREE.PlaneGeometry(10, 300);
            const roadMat = new THREE.MeshStandardMaterial({ color: 0xffcc00, roughness: 0.4 });
            const road = new THREE.Mesh(roadGeo, roadMat);
            road.rotation.x = -Math.PI / 2;
            road.position.z = -100;
            scene.add(road);

            // 6. Tạo nhân vật Gián (Màu xanh/xám nhỏ gọn phía trước)
            const playerGeo = new THREE.BoxGeometry(0.8, 0.8, 1.2);
            const playerMat = new THREE.MeshStandardMaterial({ color: 0x2ed573 });
            player = new THREE.Mesh(playerGeo, playerMat);
            player.position.set(lanePositions[currentLane], 0.4, 0);
            scene.add(player);

            // 7. Tạo Mèo Oggy (Kẻ đuổi bắt phía sau lưng)
            const oggyGeo = new THREE.BoxGeometry(1.2, 1.4, 1.5);
            const oggyMat = new THREE.MeshStandardMaterial({ color: 0x1e90ff }); // Xanh đặc trưng Oggy
            oggy = new THREE.Mesh(oggyGeo, oggyMat);
            oggy.position.set(0, 0.7, 2.5);
            scene.add(oggy);

            // Xử lý phím điều khiển
            window.addEventListener('keydown', handleKeyPress);

            animate();
        }

        function handleKeyPress(e) {
            if (gameOver) return;
            if ((e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') && currentLane > 0) {
                currentLane--;
            }
            if ((e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') && currentLane < 2) {
                currentLane++;
            }
        }

        function spawnObstacle() {
            const lane = Math.floor(Math.random() * 3);
            const obsGeo = new THREE.BoxGeometry(1.5, 1.2, 1.2);
            const obsMat = new THREE.MeshStandardMaterial({ color: 0xff4757 }); // Chướng ngại vật màu đỏ
            const obstacle = new THREE.Mesh(obsGeo, obsMat);
            obstacle.position.set(lanePositions[lane], 0.6, -80);
            scene.add(obstacle);
            obstacles.push(obstacle);
        }

        let frameCounter = 0;
        function animate() {
            if (gameOver) return;

            requestAnimationFrame(animate);

            // Di chuyển vị trí gián mượt mà theo làn
            let targetX = lanePositions[currentLane];
            player.position.x += (targetX - player.position.x) * 0.2;

            // Mèo Oggy bám sát đằng sau
            oggy.position.x += (player.position.x - oggy.position.x) * 0.1;

            // Sinh chướng ngại vật định kỳ
            frameCounter++;
            if (frameCounter > 70) {
                spawnObstacle();
                frameCounter = 0;
                score += 5;
                document.getElementById('scoreVal').innerText = score;
                gameSpeed += 0.002; // Tăng tốc dần
            }

            // Cập nhật chướng ngại vật lao tới
            for (let i = obstacles.length - 1; i >= 0; i--) {
                let obs = obstacles[i];
                obs.position.z += gameSpeed * 25;

                // Kiểm tra va chạm (Va vào chướng ngại vật là thua)
                let dist = player.position.distanceTo(obs.position);
                if (dist < 1.1) {
                    triggerGameOver();
                }

                // Xóa chướng ngại vật khi chạy qua màn hình
                if (obs.position.z > 5) {
                    scene.remove(obs);
                    obstacles.splice(i, 1);
                }
            }

            renderer.render(scene, camera);
        }

        function triggerGameOver() {
            gameOver = true;
            document.getElementById('finalScore').innerText = score;
            document.getElementById('gameOverScreen').style.display = 'flex';
        }

        function restartGame() {
            // Xóa hết chướng ngại vật cũ
            obstacles.forEach(obs => scene.remove(obs));
            obstacles = [];
            
            score = 0;
            gameSpeed = 0.3;
            currentLane = 1;
            player.position.x = lanePositions[1];
            document.getElementById('scoreVal').innerText = score;
            
            gameOver = false;
            document.getElementById('gameOverScreen').style.display = 'none';
            animate();
        }

        window.onload = init;
    </script>
</body>
</html>
"""

components.html(game_html, height=530)
