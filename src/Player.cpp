#include "Player.hpp"

Player::Player() : x(0), y(0) {}

void Player::move(int dx, int dy) {
    x += dx;
    y += dy;
}

int Player::getX() const { return x; }
int Player::getY() const { return y; }
