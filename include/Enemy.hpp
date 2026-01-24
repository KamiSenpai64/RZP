#pragma once

class Enemy {
public:
    Enemy();
    void moveRandom();
    int getX() const;
    int getY() const;
private:
    int x, y;
};
