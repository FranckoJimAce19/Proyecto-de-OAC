#pragma once
#include "constants.h"

#ifdef SKIERDLL_EXPORTS
#define SKIERDLL_API __declspec(dllexport)
#else
#define SKIERDLL_API __declspec(dllexport)
#endif

#ifdef __cplusplus
extern "C" {
#endif

	typedef struct {
		int direction;
		int rect_center_x;
		int rect_center_y;
		int speed_x;
		int speed_y;
		int lives;
	} Skier;

	typedef struct {
		int location_x;
		int location_y;
		char attribute[20];
		bool passed;
	} Obstacle;

	typedef struct {
		int distance;
		int score;
		int obstaclesFlag;
		int added_trees;
		int added_flags;
		int base_speed;
		int speed_bonus;
	} GameState;

	//Skier
	SKIERDLL_API Skier* Skier_create();
	SKIERDLL_API void Skier_turn(Skier* skier, int num);
	SKIERDLL_API void Skier_move(Skier* skier);
	SKIERDLL_API void Skier_setForward(Skier* skier);
	SKIERDLL_API int Skier_getDirection(Skier* skier);
	SKIERDLL_API void Skier_getPosition(Skier* skier, int* x, int* y);
	SKIERDLL_API void Skier_getSpeed(Skier* skier, int* speed_x, int* speed_y);
	SKIERDLL_API int Skier_getLives(Skier* skier);

	//Obstacle
	SKIERDLL_API Obstacle* Obstacle_create(int location_x, int location_y, const char* attribute);
	SKIERDLL_API int Obstacle_move(Obstacle* obstacle, int num);
	SKIERDLL_API void Obstacle_getPosition(Obstacle* obstacle, int* x, int* y);
	SKIERDLL_API void Obstacle_setPosition(Obstacle* obstacle, int x, int y);
	SKIERDLL_API const char* Obstacle_getAttribute(Obstacle* obstacle);
	SKIERDLL_API bool Obstacle_getPassed(Obstacle* obstacle);
	SKIERDLL_API void Obstacle_setPassed(Obstacle* obstacle, bool passed);

	//Obstacles
	SKIERDLL_API void srand_asm();
	SKIERDLL_API int rand_asm();
	SKIERDLL_API void createObstacles(int start_row, int end_row, int num, const char* obs_type, int(*locations)[2], char(*atrtributes)[20], int* num_obstacles);
	SKIERDLL_API void updateObstacles(int score, int* added_trees, int* added_flags);

	//Speed
	SKIERDLL_API void updateSpeed(int score, int* speed_bonus, int* base_speed,
		const int* speed_levels, int levels_count, int* achieved_levels,
		int* achieved_count, int direction, int* current_speed);

	//GameState
	SKIERDLL_API GameState* GameState_create();
	SKIERDLL_API void GameState_updateDistance(GameState* state, int speed_y);
	SKIERDLL_API void GameState_addScore(GameState* state, int points);
	SKIERDLL_API int updateObstaclesCycle(GameState* state, int speed_y);
	SKIERDLL_API int checkCollision(int x1, int y1, int w1, int h1, int x2, int y2, int w2, int h2);

#ifdef __cplusplus
}
#endif