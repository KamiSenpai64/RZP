#include "Enemy.hpp"
#include <cstdlib>
#include <ctime>

Enemy::Enemy() : x(5), y(5) {
    std::srand(std::time(nullptr));
}

void Enemy::moveRandom() {
    int dx = (std::rand() % 3) - 1;
    int dy = (std::rand() % 3) - 1;
    x += dx;
    y += dy;
}

int Enemy::getX() const { return x; }
int Enemy::getY() const { return y; }
