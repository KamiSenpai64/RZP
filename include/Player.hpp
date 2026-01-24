#pragma once

class Player {
public:
    Player();
    void move(int dx, int dy);
    int getX() const;
    int getY() const;
private:
    int x, y;
};
