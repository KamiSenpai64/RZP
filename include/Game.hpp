#pragma once
#include "Player.hpp"
#include "Enemy.hpp"

class Game {
public:
    Game();
    void run();
private:
    Player player;
    Enemy enemy;
    void processInput();
    void update();
    void render();
};
