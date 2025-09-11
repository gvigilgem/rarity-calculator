<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rarity Calculator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
            background-color: #f4f4f4;
        }
        .form-section {
            background: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        select, input {
            width: 100%;
            padding: 8px;
            margin-bottom: 15px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button {
            background: #007bff;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background: #0056b3;
        }
        #calculate-btn {
            width: 100%;
            margin-top: 20px;
        }
        #thinking {
            display: none;
            text-align: center;
            font-size: 18px;
            color: #007bff;
            margin: 20px 0;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #007bff;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        #results {
            display: none;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            text-align: center;
        }
        #results h2 {
            color: #007bff;
        }
        #results p {
            font-size: 18px;
            margin: 10px 0;
        }
        .share-buttons {
            margin-top: 20px;
        }
        .share-buttons button {
            margin: 5px;
            width: auto;
        }
        #share-image {
            max-width: 100%;
            border: 1px solid #ddd;
            border-radius: 8px;
            margin-top: 10px;
        }
        .comparison {
            background: #e9ecef;
            padding: 10px;
            border-radius: 4px;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <h1>Rarity Calculator</h1>
    
    <div class="form-section">
        <h2>Your Stats</h2>
        <label for="age">Age:</label>
        <input type="number" id="age" min="0" max="100" value="0">
        
        <label for="gender">Gender:</label>
        <select id="gender">
            <option value="">Select</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
        </select>
        
        <label for="height">Height (inches):</label>
        <input type="number" id="height" min="0" max="100" value="0">
        
        <label for="weight">Weight (lbs):</label>
        <input type="number" id="weight" min="0" max="500" value="0">
        
        <!-- Add more fields as needed, e.g., race, ethnicity, etc. – all default to 0 or blank -->
        <label for="race">Race/Ethnicity:</label>
        <select id="race">
            <option value="">Select</option>
            <option value="caucasian">Caucasian</option>
            <option value="african-american">African American</option>
            <option value="hispanic">Hispanic</option>
            <option value="asian">Asian</option>
            <option value="other">Other</option>
        </select>
        
        <label for="name">Your Name:</label>
        <input type="text" id="name" placeholder="Enter your name">
    </div>
    
    <div class="form-section">
        <h2>Compare to Ex (Optional)</h2>
        <label for="ex-age">Ex's Age:</label>
        <input type="number" id="ex-age" min="0" max="100" value="0">
        
        <label for="ex-gender">Ex's Gender:</label>
        <select id="ex-gender">
            <option value="">Select</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
        </select>
        
        <label for="ex-height">Ex's Height (inches):</label>
        <input type="number" id="ex-height" min="0" max="100" value="0">
        
        <label for="ex-weight">Ex's Weight (lbs):</label>
        <input type="number" id="ex-weight" min="0" max="500" value="0">
        
        <label for="ex-race">Ex's Race/Ethnicity:</label>
        <select id="ex-race">
            <option value="">Select</option>
            <option value="caucasian">Caucasian</option>
            <option value="african-american">African American</option>
            <option value="hispanic">Hispanic</option>
            <option value="asian">Asian</option>
            <option value="other">Other</option>
        </select>
        
        <label for="ex-name">Ex's Name:</label>
        <input type="text" id="ex-name" placeholder="Enter ex's name">
    </div>
    
    <button id="calculate-btn">Calculate Rarity</button>
    
    <div id="thinking">
        <div class="spinner"></div>
        <p>Thinking... Generating your unique rarity score!</p>
    </div>
    
    <div id="results">
        <h2 id="result-title">Your Rarity Results</h2>
        <p id="result-text">Based on your stats, you are in the top <span id="rarity-percent">0.01%</span> of rarity! This means you're one in a million (literally).</p>
        <div id="comparison" class="comparison" style="display: none;">
            <p>Compared to <span id="ex-name-display"></span>, you're <span id="comparison-text">even rarer!</span></p>
        </div>
        <div class="share-buttons">
            <button id="copy-btn">Copy to Share</button>
            <button id="share-btn">Share Image</button>
        </div>
        <canvas id="share-canvas" style="display: none;"></canvas>
        <img id="share-image" style="display: none;" alt="Share this!">
    </div>

    <script>
        // Simple rarity calculation function (expand with real weights/logic)
        function calculateRarity(stats, isComparison = false) {
            // Placeholder logic: rarity based on age, height, weight, etc.
            // In reality, use a weighted formula, e.g., rarity = 1 / (product of probabilities)
            let score = 1000000; // Base "one in a million"
            score *= Math.abs(stats.age - 30) / 100; // Age deviation
            score *= Math.abs(stats.height - 68) / 10; // Height from avg
            score *= Math.abs(stats.weight - 170) / 50; // Weight from avg
            // Add more factors...
            return Math.max(1000, score); // Min rarity 1 in 1000
        }

        document.getElementById('calculate-btn').addEventListener('click', function() {
            const name = document.getElementById('name').value || 'You';
            const exName = document.getElementById('ex-name').value || '';
            
            // Hide results, show thinking
            document.getElementById('results').style.display = 'none';
            document.getElementById('thinking').style.display = 'block';
            document.getElementById('calculate-btn').disabled = true;
            
            // 3-second delay for drama
            setTimeout(() => {
                // Collect stats
                const userStats = {
                    age: parseInt(document.getElementById('age').value) || 0,
                    gender: document.getElementById('gender').value,
                    height: parseInt(document.getElementById('height').value) || 0,
                    weight: parseInt(document.getElementById('weight').value) || 0,
                    race: document.getElementById('race').value,
                    name: name
                };
                
                let rarity = calculateRarity(userStats);
                let percent = (1 / rarity * 100).toFixed(4);
                
                document.getElementById('rarity-percent').textContent = percent + '%';
                document.getElementById('result-title').textContent = name + '\'s Rarity Results';
                document.getElementById('result-text').innerHTML = `Based on your stats, ${name} is in the top <span id="rarity-percent">${percent}%</span> of rarity! This means you're one in ${Math.round(rarity)}.`;
                
                // Handle comparison if ex stats provided
                let comparisonDiv = document.getElementById('comparison');
                if (exName) {
                    const exStats = {
                        age: parseInt(document.getElementById('ex-age').value) || 0,
                        gender: document.getElementById('ex-gender').value,
                        height: parseInt(document.getElementById('ex-height').value) || 0,
                        weight: parseInt(document.getElementById('ex-weight').value) || 0,
                        race: document.getElementById('ex-race').value,
                        name: exName
                    };
                    let exRarity = calculateRarity(exStats);
                    let comparisonPercent = (1 / exRarity * 100).toFixed(4);
                    
                    document.getElementById('ex-name-display').textContent = exName;
                    if (rarity > exRarity) {
                        document.getElementById('comparison-text').textContent = `rarer than ${exName} (who is ${comparisonPercent}%)!`;
                    } else {
                        document.getElementById('comparison-text').textContent = `as rare as ${exName} (both ${percent}%)!`;
                    }
                    comparisonDiv.style.display = 'block';
                } else {
                    comparisonDiv.style.display = 'none';
                }
                
                // Show results
                document.getElementById('thinking').style.display = 'none';
                document.getElementById('results').style.display = 'block';
                document.getElementById('calculate-btn').disabled = false;
                
                // Generate share image
                generateShareImage();
            }, 3000);
        });
        
        function generateShareImage() {
            const canvas = document.getElementById('share-canvas');
            const ctx = canvas.getContext('2d');
            canvas.width = 800;
            canvas.height = 400;
            
            // Background
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(0, 0, 800, 400);
            
            // Title
            ctx.fillStyle = '#007bff';
            ctx.font = 'bold 32px Arial';
            ctx.textAlign = 'center';
            ctx.fillText('Your Rarity Score!', 400, 60);
            
            // Rarity text
            ctx.fillStyle = '#333';
            ctx.font = '24px Arial';
            const rarityText = document.getElementById('result-text').textContent;
            ctx.fillText(rarityText, 400, 120);
            
            // Comparison if present
            const comparison = document.getElementById('comparison-text').textContent;
            if (comparison) {
                ctx.fillText(comparison, 400, 180);
            }
            
            // Footer
            ctx.fillStyle = '#666';
            ctx.font = '16px Arial';
            ctx.fillText('Generated by Rarity Calculator', 400, 360);
            
            // Convert to image
            const img = document.getElementById('share-image');
            img.src = canvas.toDataURL('image/png');
            img.style.display = 'block';
        }
        
        document.getElementById('copy-btn').addEventListener('click', function() {
            const text = document.getElementById('result-text').textContent + (document.getElementById('comparison-text').textContent ? '\n' + document.getElementById('comparison-text').textContent : '');
            navigator.clipboard.writeText(text).then(() => {
                alert('Copied to clipboard!');
            });
        });
        
        document.getElementById('share-btn').addEventListener('click', function() {
            const img = document.getElementById('share-image');
            img.style.display = 'block';
            // For actual sharing, you could use Web Share API or just prompt download
            const link = document.createElement('a');
            link.download = 'rarity-score.png';
            link.href = img.src;
            link.click();
            
            // Reset form
            resetForm();
        });
        
        function resetForm() {
            document.querySelectorAll('input, select').forEach(el => {
                if (el.type === 'number') el.value = 0;
                else if (el.tagName === 'SELECT') el.selectedIndex = 0;
                else el.value = '';
            });
            document.getElementById('results').style.display = 'none';
            document.getElementById('share-image').style.display = 'none';
        }
    </script>
</body>
</html>
