#include "Game.hpp"
#include <iostream>

Game::Game() {}

void Game::run() {
    while (true) {
        processInput();
        update();
        render();
    }
}

void Game::processInput() {
    char input;
    std::cout << "Enter move (w/a/s/d or q to quit): ";
    std::cin >> input;

    if (input == 'q') std::exit(0);
    else if (input == 'w') player.move(0, -1);
    else if (input == 's') player.move(0, 1);
    else if (input == 'a') player.move(-1, 0);
    else if (input == 'd') player.move(1, 0);
}

void Game::update() {
    enemy.moveRandom();
}

void Game::render() {
    std::cout << "Player at (" << player.getX() << ", " << player.getY() << ")\n";
    std::cout << "Enemy at (" << enemy.getX() << ", " << enemy.getY() << ")\n";
}
