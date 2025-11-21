#include "pch.h"
#include <math.h>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <float.h>
#include "lib_logic.Skier.h"
#include "constants.h"

//Skier
SKIERDLL_API Skier* Skier_create() {
    Skier* skier = (Skier*)malloc(sizeof(Skier));
    skier->direction = 0;
    skier->rect_center_x = 320;
    skier->rect_center_y = 100;
    skier->speed_x = skier->direction;
    skier->speed_y = 6 - abs(skier->direction) * 2;
    skier->lives = 3;
    return skier;
}

SKIERDLL_API void Skier_turn(Skier* skier, int num) {
    skier->direction += num;
    if (skier->direction < -2) skier->direction = -2;
    if (skier->direction > 2) skier->direction = 2;
    skier->speed_x = skier->direction;
    skier->speed_y = 6 - abs(skier->direction) * 2;
}
SKIERDLL_API void Skier_move(Skier* skier) {
    skier->rect_center_x += skier->speed_x;
    if (skier->rect_center_x < 20) skier->rect_center_x = 20;
    if (skier->rect_center_x > 620) skier->rect_center_x = 620;
}
SKIERDLL_API void Skier_setForward(Skier* skier) {
    skier->direction = 0;
    skier->speed_x = skier->direction;
    skier->speed_y = 6 - abs(skier->direction) * 2;
}
SKIERDLL_API int Skier_getDirection(Skier* skier) {
    return skier->direction;
}
SKIERDLL_API void Skier_getPosition(Skier* skier, int* x, int* y) {
    *x = skier->rect_center_x;
    *y = skier->rect_center_y;
}
SKIERDLL_API void Skier_getSpeed(Skier* skier, int* speed_x, int* speed_y) {
    *speed_x = skier->speed_x;
    *speed_y = skier->speed_y;
}
SKIERDLL_API int Skier_getLives(Skier* skier) {
    return skier->lives;
}

//Obstacle
SKIERDLL_API Obstacle* Obstacle_create(int location_x, int location_y, const char* attribute) {
    Obstacle* obstacle = (Obstacle*)malloc(sizeof(Obstacle));
    if (!obstacle) return nullptr;
    obstacle->location_x = location_x;
    obstacle->location_y = location_y;
    if (attribute) {
        strncpy_s(obstacle->attribute, attribute, sizeof(obstacle->attribute) - 1);
        obstacle->attribute[sizeof(obstacle->attribute) - 1] = '\0';
    } else {
        obstacle->attribute[0] = '\0';
    }
    obstacle->passed = false;
    return obstacle;
}
SKIERDLL_API int Obstacle_move(Obstacle* obstacle, int num) {
    return obstacle->location_y - num;
}
SKIERDLL_API void Obstacle_getPosition(Obstacle* obstacle, int* x, int* y) {
    *x = obstacle->location_x;
    *y = obstacle->location_y;
}
SKIERDLL_API void Obstacle_setPosition(Obstacle* obstacle, int x, int y) {
    obstacle->location_x = x;
    obstacle->location_y = y;
}
SKIERDLL_API const char* Obstacle_getAttribute(Obstacle* obstacle) {
    return obstacle->attribute;
}
SKIERDLL_API bool Obstacle_getPassed(Obstacle* obstacle) {
    return obstacle->passed;
}
SKIERDLL_API void Obstacle_setPassed(Obstacle* obstacle, bool passed) {
    obstacle->passed = passed;
}

//Obstacles_mechanics
SKIERDLL_API void createObstacles(int start_row, int end_row, int num, const char* obs_type, int(*locations)[2], char(*attributes)[20], int* num_obstacles) {
    srand((unsigned int) time(NULL));
    int ref = num;
    int count = 0;
    for (int i = 0; i < 10 + num; i++) {
        int row = rand() % (end_row - start_row + 1) + start_row;
        int col = rand() % 10;
        int location_x = col * 64 + 20;
        int location_y = row * 64 + 20;
        bool exists = false;
        for (int j = 0; j < count; j++) {
            if (locations[j][0] == location_x && locations[j][1] == location_y) {
                exists = true;
                break;
            }
        }
        if (!exists) {
            locations[count][0] = location_x;
            locations[count][1] = location_y;
            if (((strcmp(obs_type, "tree") == 0) || strcmp(obs_type, "flag") == 0) && (ref != 0 && ref <= num)) {
                strcpy_s(attributes[count], 20, obs_type);
                ref--;
            } else {
                const char* possible_attributes[] = { "tree", "flag" };
                int random_index = rand() % 2;
                strcpy_s(attributes[count], 20, possible_attributes[random_index]);

            }
            count++;
        }
    }
    *num_obstacles = count;
}
SKIERDLL_API void updateObstacles(int score, int* added_trees, int* added_flags) {
    if (score > 0 && score % 150 == 0 && *added_trees < 20) {
        *added_trees += 2;
    }
    if (score > 0 && score % 200 == 0 && *added_flags < 10) {
        *added_flags += 1;
    }
}
//Speed
SKIERDLL_API void updateSpeed(int score, int* speed_bonus, int* base_speed,
    const int* speed_levels, int levels_count, int* achieved_levels,
    int* achieved_count, int direction, int* current_speed) {
    for (int i = 0; i < levels_count; i++) {
        int level = speed_levels[i];
        if (score >= level) {
            int already_achieved = 0;
            for (int j = 0; j < *achieved_count; j++) {
                if (achieved_levels[j] == level) {
                    already_achieved = 1;
                    break;
                }
            }
            if (!already_achieved) {
                achieved_levels[(*achieved_count)++] = level;
                (*speed_bonus)++;
                (*base_speed)++;
            }
        }
    }
    *current_speed = *base_speed - abs(direction) * 2;
}

//GameState
SKIERDLL_API GameState* GameState_create() {
    GameState* state = (GameState*)malloc(sizeof(GameState));
    if (!state) return nullptr;
    state->distance = 0;
    state->score = 0;
    state->obstaclesFlag = 0;
    state->added_trees = 0;
    state->added_flags = 0;
    state->base_speed = 7;
    state->speed_bonus = 0;
    return state;
}
SKIERDLL_API void GameState_updateDistance(GameState* state, int speed_y) {
    if (state) {
        state->distance += speed_y;
    }
}
SKIERDLL_API void GameState_addScore(GameState* state, int points) {
    if (state) {
        state->score += points;
    }
}
SKIERDLL_API int updateObstaclesCycle(GameState* state, int speed_y) {
    if (!state) return 0;
    int needs_update = 0;
    if (state->distance >= 640 && state->obstaclesFlag == 0) {
        state->obstaclesFlag = 1;
        needs_update = 1;
    }
    if (state->distance >= 1280 && state->obstaclesFlag == 1) {
        state->obstaclesFlag = 0;
        state->distance -= 1280;
        needs_update = 2;
    }
    return needs_update;
}
SKIERDLL_API int checkCollision(
    int x1, int y1, int w1, int h1,
    int x2, int y2, int w2, int h2
) {
    int overlapX = (x1 < x2 + w2) && (x1 + w1 > x2);
    int overlapY = (y1 < y2 + h2) && (y1 + h1 > y2);
    
    return overlapX && overlapY;
}
