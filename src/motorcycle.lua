```lua
--[[
    Motorcycle Game - MVP Implementation (Scoring, Rounds)

    This script provides a basic motorcycle game loop with scoring and rounds.

    Modules:
    - MotorcycleController: Handles motorcycle movement and physics.
    - RoundManager: Manages round start, end, and round number.
    - ScoreManager: Tracks the player's score.
    - UIManager: Updates the UI with round number, score and messages.
]]

-- Services
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")

--// MODULES \\--

-- Module for handling motorcycle movement and physics
local MotorcycleController = require(script:WaitForChild("MotorcycleController")) -- Replace "MotorcycleController" with the actual name of the module script
-- Module for managing rounds
local RoundManager = require(script:WaitForChild("RoundManager")) -- Replace "RoundManager" with the actual name of the module script
-- Module for managing scoring
local ScoreManager = require(script:WaitForChild("ScoreManager")) -- Replace "ScoreManager" with the actual name of the module script
-- Module for updating the UI
local UIManager = require(script:WaitForChild("UIManager")) -- Replace "UIManager" with the actual name of the module script


--// VARIABLES \\--

local motorcycleModelName = "Motorcycle" -- Name of the motorcycle model in Workspace
local startingPointName = "StartingPoint" -- Name of the starting point part
local endPointName = "EndPoint" -- Name of the end point part.

local motorcycle
local startingPoint
local endPoint

-- Game parameters
local scorePerRound = 100 -- Score awarded for completing a round
local timeBetweenRounds = 3 -- Time in seconds before the next round starts
local initialRoundNumber = 1


--// FUNCTION DEFINITIONS \\--

local function setupGame()
    -- Find the Motorcycle model
    motorcycle = workspace:FindFirstChild(motorcycleModelName)
    if not motorcycle then
        error("Motorcycle model not found in Workspace!")
        return false
    end

    -- Find the StartingPoint
    startingPoint = workspace:FindFirstChild(startingPointName)
    if not startingPoint then
        error("StartingPoint part not found in Workspace!")
        return false
    end

    -- Find the EndPoint
    endPoint = workspace:FindFirstChild(endPointName)
    if not endPoint then
        error("EndPoint part not found in Workspace!")
        return false
    end

    -- Initialize modules
    MotorcycleController.init(motorcycle)
    RoundManager.init(initialRoundNumber)
    ScoreManager.init()
    UIManager.init() -- Assuming UIManager handles its own canvas setup

    return true
end


local function startRound()
    -- Reset Motorcycle Position
    motorcycle:SetPrimaryPartCFrame(startingPoint.CFrame)
    MotorcycleController.resetVelocity()

    -- Enable Motorcycle Controls
    MotorcycleController.enableControls()

    -- Update UI
    UIManager.displayMessage("Round " .. RoundManager.getCurrentRound() .. " Started!")
end

local function endRound()
    -- Disable Motorcycle Controls
    MotorcycleController.disableControls()

    -- Award score for completing the round
    ScoreManager.addScore(scorePerRound)

    -- Update UI
    UIManager.displayMessage("Round " .. RoundManager.getCurrentRound() .. " Completed! +" .. scorePerRound .. " Points")
    UIManager.updateScore(ScoreManager.getScore())

    -- Increment round number
    RoundManager.nextRound()
end

local function gameLoop()
    -- Main game loop that runs continuously
    while true do
        -- Start a new round
        startRound()

        -- Wait until the player reaches the end point (simple collision detection)
        local connection

        local function checkCollision(part)
           if part:IsDescendantOf(motorcycle) then
               endRound()
               connection:Disconnect()
               return
           end
        end

        connection = endPoint.Touched:Connect(checkCollision)


        -- Wait a specified amount of time or until the round is over, whichever comes first.
        -- In a real game you would likely have level conditions, timer etc.
        -- Use RunService.Heartbeat to check frame by frame if needed

        wait(15) -- Placeholder - Should be based on some game condition not a fixed time!
        -- If player didn't reach end point during that time, end the round
        if connection then
            connection:Disconnect()
            endRound()
            UIManager.displayMessage("Round failed.") -- Example message.
        end


        -- Wait before starting the next round
        wait(timeBetweenRounds)

    end
end


--// INITIALIZATION \\--

-- Main function to start the game
local function startGame()
    if not setupGame() then
        return -- Exit if setup fails
    end

    -- Start the main game loop in a separate thread to avoid blocking
    task.spawn(gameLoop)
end

-- Call startGame when the script is run.
startGame()
```

**Explanation and Improvements:**

1. **Modular Design:** The code is now broken down into modules (`MotorcycleController`, `RoundManager`, `ScoreManager`, `UIManager`) which each handle specific aspects of the game.  This makes the code more organized, reusable, and easier to maintain. **Crucially, you need to create and populate those module scripts** with the corresponding logic.  I provide placeholders in the `require()` statements, replace these with the actual module names.

2. **Clear Separation of Concerns:**  Each module focuses on a single responsibility (movement, rounds, score, UI).

3. **Roblox Services:** Uses `game:GetService()` to properly get important Roblox services.

4. **Error Handling:** Includes `error()` calls with informative messages when required parts are not found.  This helps in debugging. The main `setupGame` function also returns a boolean to indicate success or failure.

5. **Comments:**  Extensive comments explain the purpose of each section and important lines of code.

6. **MotorcycleController Module (Example - you MUST implement this):**
   ```lua
   -- ReplicatedStorage.MotorcycleController

   local MotorcycleController = {}

   local motorcycle -- The motorcycle model
   local controlsEnabled = false

   function MotorcycleController.init(motorcycleModel)
       motorcycle = motorcycleModel

       -- Initialize any physics or movement related settings for the motorcycle
       -- Example:
       -- motorcycle.PrimaryPart.AssemblyLinearVelocity = Vector3.new(0, 0, 0)

   end

   function MotorcycleController.enableControls()
       controlsEnabled = true
       -- Connect input events to control the motorcycle's movement
       -- Example (using UserInputService):
       -- local UserInputService = game:GetService("UserInputService")
       -- local function onInputBegan(input, gameProcessedEvent)
       --    if not controlsEnabled or gameProcessedEvent then return end
       --    if input.KeyCode == Enum.KeyCode.W then
       --       -- Apply forward force to the motorcycle
       --    end
       -- end
       -- UserInputService.InputBegan:Connect(onInputBegan)

       -- Consider using ContextActionService for more robust input handling
   end

   function MotorcycleController.disableControls()
       controlsEnabled = false
       -- Disconnect any input events to disable movement
       -- (Implement disconnection of input handlers here)
   end

   function MotorcycleController.resetVelocity()
      if motorcycle then
          motorcycle.PrimaryPart.AssemblyLinearVelocity = Vector3.new(0, 0, 0)
          motorcycle.PrimaryPart.AssemblyAngularVelocity = Vector3.new(0, 0, 0)
      end
   end

   return MotorcycleController
   ```

7. **RoundManager Module (Example - you MUST implement this):**
   ```lua
   -- ReplicatedStorage.RoundManager

   local RoundManager = {}

   local currentRound = 0

   function RoundManager.init(initialRound)
       currentRound = initialRound or 1
   end

   function RoundManager.getCurrentRound()
       return currentRound
   end

   function RoundManager.nextRound()
       currentRound = currentRound + 1
   end

   return RoundManager
   ```

8. **ScoreManager Module (Example - you MUST implement this):**
   ```lua
   -- ReplicatedStorage.ScoreManager

   local ScoreManager = {}

   local playerScore = 0

   function ScoreManager.init()
       playerScore = 0
   end

   function ScoreManager.addScore(score)
       playerScore = playerScore + score
   end

   function ScoreManager.getScore()
       return playerScore
   end

   return ScoreManager
   ```

9. **UIManager Module (Example - you MUST implement this):**
   ```lua
   -- ReplicatedStorage.UIManager

   local UIManager = {}

   local screenGui -- The ScreenGui object
   local scoreLabel -- TextLabel for displaying score
   local roundLabel -- TextLabel for displaying round
   local messageLabel -- TextLabel for displaying messages

   function UIManager.init()
       -- Create UI elements if they don't exist (or find existing ones)
       -- Example:
       screenGui = Instance.new("ScreenGui")
       screenGui.Name = "MotorcycleUI"
       screenGui.Parent = game.Players.LocalPlayer:WaitForChild("PlayerGui") -- Use PlayerGui

       -- Ensure all UI elements are created *within* the ScreenGui.
       scoreLabel = Instance.new("TextLabel")
       scoreLabel.Name = "ScoreLabel"
       scoreLabel.Size = UDim2.new(0, 200, 0, 30)
       scoreLabel.Position = UDim2.new(0, 10, 0, 10)
       scoreLabel.BackgroundTransparency = 1
       scoreLabel.TextColor3 = Color3.new(1, 1, 1)
       scoreLabel.Text = "Score: 0"
       scoreLabel.Parent = screenGui

       roundLabel = Instance.new("TextLabel")
       roundLabel.Name = "RoundLabel"
       roundLabel.Size = UDim2.new(0, 200, 0, 30)
       roundLabel.Position = UDim2.new(0, 10, 0, 50)
       roundLabel.BackgroundTransparency = 1
       roundLabel.TextColor3 = Color3.new(1, 1, 1)
       roundLabel.Text = "Round: 1"
       roundLabel.Parent = screenGui

       messageLabel = Instance.new("TextLabel")
       messageLabel.Name = "MessageLabel"
       messageLabel.Size = UDim2.new(0, 300, 0, 50)
       messageLabel.Position = UDim2.new(0.5, -150, 0, 100) -- Centered horizontally
       messageLabel.BackgroundTransparency = 1
       messageLabel.TextColor3 = Color3.new(1, 1, 0) -- Yellow
       messageLabel.Text = ""
       messageLabel.TextScaled = true
       messageLabel.TextWrapped = true
       messageLabel.Parent = screenGui
   end

   function UIManager.updateScore(score)
       scoreLabel.Text = "Score: " .. score
   end

   function UIManager.updateRound(round)
       roundLabel.Text = "Round: " .. round
   end

   function UIManager.displayMessage(message)
       messageLabel.Text = message
       task.delay(3, function() messageLabel.Text = "" end) -- Clear message after 3 seconds
   end

   return UIManager
   ```

10. **`MotorcycleController.enableControls()` Placeholder:** The `MotorcycleController.enableControls()` function *requires* you to implement the actual input handling logic.  You'll need to use `UserInputService` or `ContextActionService` to detect key presses and apply forces/torques to the motorcycle to move it.  This is the most complex part. The above example comments show usage of `UserInputService`.

11. **Collision Detection:** Uses a simple `Touched` event on the `endPoint` part to detect when the motorcycle reaches the end.  **Important:**  Make sure the `endPoint`'s `CanCollide` property is set to `true` for this to work, and that the motorcycle has parts that will collide with it. The code checks if the part touching the `endPoint` is part of the motorcycle.

12. **`wait()` Replacement:** The `wait(15)` inside the `gameLoop` is a *placeholder*.  You *must* replace this with a more appropriate condition to determine when a round should end.  Examples:
    *   A timer (using `tick()` or `os.time()`).
    *   A complex collision system involving multiple checkpoints.
    *   A user input (e.g., the player presses a "Give Up" button).
    *  Checking for the presence of the character at the End Point.
    * RunService.Heartbeat with delta time

13. **Local Script:**  This code should be placed in a **LocalScript** inside `StarterPlayerScripts`.  The `UIManager` needs to access the `PlayerGui`, which can only be done reliably from a LocalScript.

14. **Server-Side Considerations:** If you need to handle scoring, leaderboards, or anti-cheat measures, you'll need to use RemoteEvents to communicate between the client (where the motorcycle controls are handled) and the server. This MVP focuses on client-side logic for simplicity.

15. **Motorcycle Model:** Ensure the motorcycle model has a `PrimaryPart` set. This is crucial for moving the entire model. The `PrimaryPart` should be a `Part` that is physically simulated (e.g., not `Anchored`).

16. **Folder Structure:** Create the following structure in your Roblox game:

   *   `StarterPlayerScripts`
       *   `MainGameScript` (This script - the one with the `startGame()` function)
   *   `ReplicatedStorage`
       *   `MotorcycleController` (ModuleScript)
       *   `RoundManager` (ModuleScript)
       *   `ScoreManager` (ModuleScript)
       *   `UIManager` (ModuleScript)
   *   `Workspace`
       *   `Motorcycle` (Model)  <-- Ensure PrimaryPart is set!
       *   `StartingPoint` (Part)
       *   `EndPoint` (Part)

**How to Use:**

1.  Create the folder structure and scripts as described above.
2.  Copy and paste the code for each module into the corresponding ModuleScript.
3.  Copy and paste the main script into the `MainGameScript` LocalScript.
4.  Design your motorcycle model, starting point, and end point in the Workspace. Make sure the names match the `motorcycleModelName`, `startingPointName`, and `endPointName` variables in the `MainGameScript`.  The motorcycle *must* have a `PrimaryPart` set.
5.  **Implement the movement logic in the `MotorcycleController.enableControls()` function.**  This is the core game mechanic!
6.  Adjust the game parameters (`scorePerRound`, `timeBetweenRounds`, `initialRoundNumber`) to your liking.
7.  Test your game!

This improved version provides a much more solid foundation for building your motorcycle game.  Remember to thoroughly test and debug your code as you add more features.  Good luck!
