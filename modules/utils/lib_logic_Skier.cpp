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
    Skier* skier;
    __asm {
        PUSH 24
        CALL malloc
        ADD ESP, 4
        MOV skier, eax

        TEST EAX, EAX
        JZ END_CREATE

        MOV DWORD PTR [EAX], 0
        MOV DWORD PTR [EAX + 4], 320
        MOV DWORD PTR [EAX + 8], 100
        MOV ECX, DWORD PTR [EAX]
        MOV DWORD PTR [EAX + 12], ECX

        MOV EDX, DWORD PTR [EAX]
        MOV EBX, EDX
        SAR EBX, 31
        XOR EDX, EBX
        SUB EDX, EBX
        IMUL EDX, 2
        MOV ECX, 6
        SUB ECX, EDX
        MOV DWORD PTR [EAX + 16], ECX

        MOV DWORD PTR [EAX + 20], 3
        END_CREATE:
    }
    return skier;
}

SKIERDLL_API void Skier_turn(Skier* skier, int num) {
    __asm {
        MOV EAX, skier
        MOV ECX, num
        ADD DWORD PTR [EAX], ECX
        MOV EDX, DWORD PTR [EAX]

        CMP EDX, -2
        JGE CHECK_UPPER
        MOV DWORD PTR [EAX], -2
        MOV EDX, -2

        CHECK_UPPER:
            CMP EDX, 2
            JLE UPDATE_SPEED
            MOV DWORD PTR [EAX], 2
            MOV EDX, 2
        
        UPDATE_SPEED:
            MOV DWORD PTR [EAX + 12], EDX

        MOV EBX, EDX
        SAR EBX, 31
        XOR EDX, EBX
        SUB EDX, EBX
        IMUL EDX, 2
        MOV ECX, 6
        SUB ECX, EDX
        MOV DWORD PTR [EAX + 16], ECX
    }
}
SKIERDLL_API void Skier_move(Skier* skier) {
    __asm {
        MOV EAX, skier
        MOV ECX, DWORD PTR [EAX + 12]
        ADD DWORD PTR [EAX + 4], ECX
        MOV EDX, DWORD PTR [EAX + 4]

        CMP EDX, 20
        JGE CHECK_UPPER
        MOV DWORD PTR [EAX + 4], 20
        MOV EDX, 20

        CHECK_UPPER:
            CMP EDX, 620
            JLE END_MOVE
            MOV DWORD PTR [EAX + 4], 620

        END_MOVE:
    }
}
SKIERDLL_API void Skier_setForward(Skier* skier) {
    __asm {
        MOV EAX, skier
        MOV DWORD PTR [EAX], 0
        MOV DWORD PTR [EAX + 12], 0
        MOV DWORD PTR [EAX + 16], 0
    }
}
SKIERDLL_API int Skier_getDirection(Skier* skier) {
    int result;
    __asm {
        MOV EAX, skier
        MOV ECX, DWORD PTR [EAX]
        MOV result, ECX
    }
    return result;
}
SKIERDLL_API void Skier_getPosition(Skier* skier, int* x, int* y) {
    __asm {
        MOV EAX, skier
        MOV EBX, x
        MOV ECX, y

        MOV EDX, DWORD PTR [EAX + 4]
        MOV DWORD PTR [EBX], EDX

        MOV EDX, DWORD PTR [EAX + 8]
        MOV DWORD PTR [ECX], EDX
    }
}
SKIERDLL_API void Skier_getSpeed(Skier* skier, int* speed_x, int* speed_y) {
    __asm {
        MOV EAX, skier
        MOV EBX, speed_x
        MOV ECX, speed_y

        MOV EDX, DWORD PTR [EAX + 12]
        MOV DWORD PTR [EBX], EDX
        
        MOV EDX, DWORD PTR [EAX + 16]
        MOV DWORD PTR [ECX], EDX
    }
}
SKIERDLL_API int Skier_getLives(Skier* skier) {
    int result;
    __asm {
        MOV EAX, skier
        MOV ECX, DWORD PTR [EAX + 20]
        MOV result, ECX
    }
    return result;
}

//Obstacle
SKIERDLL_API Obstacle* Obstacle_create(int location_x, int location_y, const char* attribute) {
    Obstacle* obstacle;
    __asm {
        PUSH 32
        CALL malloc
        ADD ESP, 4
        MOV obstacle, EAX

        TEST EAX, EAX
        JZ END_CREATE

        MOV ECX, location_x
        MOV DWORD PTR [EAX], ECX

        MOV ECX, location_y
        MOV DWORD PTR [EAX + 4], ECX

        MOV ESI, attribute
        TEST ESI, ESI
        JZ SET_EMPTY

        LEA EDI, [EAX + 8]
        XOR ECX, ECX

        COPY_LOOP:
            CMP ECX, 19
            JGE TERMINATE
            MOV BL, BYTE PTR [ESI + ECX]
            MOV BYTE PTR [EDI + ECX], BL
            TEST BL, BL
            JZ SET_PASSED
            INC ECX
            JMP COPY_LOOP

        TERMINATE:
            MOV BYTE PTR [EDI + 19], 0
            JMP SET_PASSED

        SET_EMPTY:
            MOV BYTE PTR [EAX + 8], 0

        SET_PASSED:
            MOV BYTE PTR [EAX + 28], 0

        END_CREATE:
    }
    return obstacle;
}
SKIERDLL_API int Obstacle_move(Obstacle* obstacle, int num) {
    int result;
    __asm {
        MOV EAX, obstacle
        MOV ECX, num

        MOV EDX, DWORD PTR [EAX + 4]
        SUB EDX, ECX
        MOV result, EDX
    }
    return result;
}
SKIERDLL_API void Obstacle_getPosition(Obstacle* obstacle, int* x, int* y) {
    __asm {
        MOV EAX, obstacle
        MOV EBX, x
        MOV ECX, y

        MOV EDX, DWORD PTR [EAX]
        MOV DWORD PTR [EBX], EDX

        MOV EDX, DWORD PTR [EAX + 4]
        MOV DWORD PTR [ECX], EDX
    }
}
SKIERDLL_API void Obstacle_setPosition(Obstacle* obstacle, int x, int y) {
    __asm {
        MOV EAX, obstacle
        MOV ECX, x
        MOV EDX, y

        MOV DWORD PTR [EAX], ECX
        MOV DWORD PTR [EAX + 4], EDX
    }
}
SKIERDLL_API const char* Obstacle_getAttribute(Obstacle* obstacle) {
    const char* result;
    __asm {
        MOV EAX, obstacle
        LEA ECX, [EAX + 8]
        MOV result, ECX
    }
    return result;
}
SKIERDLL_API bool Obstacle_getPassed(Obstacle* obstacle) {
    bool result;
    __asm {
        MOV EAX, obstacle
        XOR ECX, ECX
        MOV CL, BYTE PTR [EAX + 28]
        MOV result, CL
    }
    return result;
}
SKIERDLL_API void Obstacle_setPassed(Obstacle* obstacle, bool passed) {
    __asm {
        MOV EAX, obstacle
        MOV CL, passed
        MOV BYTE PTR [EAX + 28], CL
    }
}

//Obstacles_mechanics
static unsigned int random_seed = 0;
SKIERDLL_API void srand_asm() {
    __asm {
        PUSH 0
        CALL time
        ADD ESP, 4
        MOV EBX, EAX
        SHL EBX, 13
        XOR EAX, EBX
        MOV EBX, EAX
        SHR EBX, 17
        XOR EAX, EBX
        MOV EBX, 0x5DEECE66D
        XOR EAX, EBX 
        MOV random_seed, EAX
    }
}
SKIERDLL_API int rand_asm() {
    //xorshift
    int result;
    __asm {
        MOV EAX, random_seed
        MOV EBX, EAX
        SHL EBX, 13
        XOR EAX, EBX
        MOV EBX, EAX
        SHR EBX, 17
        XOR EAX, EBX
        MOV EBX, EAX
        SHL EBX, 5
        XOR EAX, EBX
        MOV random_seed, EAX
        AND EAX, 0x7FFFFFFF
        MOV result, EAX
    }
    return result;
}
SKIERDLL_API void createObstacles(int start_row, int end_row, int num, const char* obs_type, int(*locations)[2], char(*attributes)[20], int* num_obstacles) {
    static int initialized = 0;
    static const char str_tree[] = "tree";
    static const char str_flag[] = "flag";
    int ref, count, loop_limit, i;
    int row, col, location_x, location_y;
    int j, exists, random_index;
    int rand_val;
    __asm {
        MOV EAX, initialized
        TEST EAX, EAX
        JNZ SEED_READY
        CALL srand_asm
        MOV initialized, 1

        SEED_READY:
            MOV ECX, num
            MOV ref, ECX
            MOV count, 0
            ADD ECX, 10
            MOV loop_limit, ECX
            MOV i, 0

        MAIN_LOOP:
            MOV EAX, i
                CMP EAX, loop_limit
                JGE END_MAIN
                CALL rand_asm
                MOV rand_val, EAX
                MOV EBX, end_row
                SUB EBX, start_row
                INC EBX
                MOV EAX, rand_val
                XOR EDX, EDX
                DIV EBX
                ADD EDX, start_row
                MOV row, EDX
                CALL rand_asm
                MOV rand_val, EAX
                MOV EAX, rand_val
                XOR EDX, EDX
                MOV ECX, 10
                DIV ECX
                MOV col, EDX
                MOV EAX, col
                IMUL EAX, 64
                ADD EAX, 20
                MOV location_x, EAX
                MOV EAX, row
                IMUL EAX, 64
                ADD EAX, 20
                MOV location_y, EAX
                MOV exists, 0
                MOV j, 0
        CHECK_LOOP:
                MOV EAX, j
                CMP EAX, count
                JGE CHECK_DONE
                IMUL EAX, 8
                MOV EBX, locations
                ADD EBX, EAX
                MOV ECX, DWORD PTR [EBX]
                CMP ECX, location_x
                JNE NOT_DUP
                MOV ECX, DWORD PTR [EBX + 4]
                CMP ECX, location_y
                JNE NOT_DUP
                MOV exists, 1
                JMP CHECK_DONE
        NOT_DUP:
                INC j
                JMP CHECK_LOOP
        CHECK_DONE:
                CMP exists, 1
                JE NEXT_ITERATION
                MOV EAX, count
                IMUL EAX, 8
                MOV EBX, locations
                ADD EBX, EAX
                MOV ECX, location_x
                MOV DWORD PTR [EBX], ECX
                MOV ECX, location_y
                MOV DWORD PTR [EBX + 4], ECX
                MOV ESI, obs_type
                LEA EDI, str_tree
                XOR ECX, ECX
        CMP_TREE:
                MOV AL, BYTE PTR [ESI + ECX]
                MOV BL, BYTE PTR [EDI + ECX]
                CMP AL, BL
                JNE TRY_FLAG
                TEST AL, AL
                JZ MATCH_FOUND
                INC ECX
                JMP CMP_TREE
        TRY_FLAG:
                MOV ESI, obs_type
                LEA EDI, str_flag
                XOR ECX, ECX
        CMP_FLAG:
                MOV AL, BYTE PTR [ESI + ECX]
                MOV BL, BYTE PTR [EDI + ECX]
                CMP AL, BL
                JNE USE_RANDOM
                TEST AL, AL
                JZ MATCH_FOUND
                INC ECX
                JMP CMP_FLAG
        MATCH_FOUND:
                MOV EAX, ref
                TEST EAX, EAX
                JZ USE_RANDOM
                CMP EAX, num
                JG USE_RANDOM
                MOV EAX, count
                IMUL EAX, 20
                MOV EDI, attributes
                ADD EDI, EAX
                MOV ESI, obs_type
                XOR ECX, ECX
        COPY_STRING:
                CMP ECX, 19
                JGE TERMINATE_STRING
                MOV BL, BYTE PTR [ESI + ECX]
                MOV BYTE PTR [EDI + ECX], BL
                TEST BL, BL
                JZ COPIED_STRING
                INC ECX
                JMP COPY_STRING
        TERMINATE_STRING:
                MOV BYTE PTR [EDI + 19], 0
        COPIED_STRING:
                MOV EAX, ref
                DEC EAX
                MOV ref, EAX
                JMP INC_COUNT
        USE_RANDOM:
                CALL rand_asm
                MOV rand_val, EAX
                MOV EAX, rand_val
                XOR EDX, EDX
                MOV ECX, 2
                DIV ECX
                MOV random_index, EDX
                CMP random_index, 0
                JE SEL_TREE
        SEL_FLAG:
                LEA ESI, str_flag
                JMP COPY_RAND
        SEL_TREE:
                LEA ESI, str_tree
        COPY_RAND:
                MOV EAX, count
                IMUL EAX, 20
                MOV EDI, attributes
                ADD EDI, EAX
                XOR ECX, ECX
        COPY_RAND_LOOP:
                CMP ECX, 19
                JGE TERMINATE_RAND
                MOV BL, BYTE PTR [ESI + ECX]
                MOV BYTE PTR [EDI + ECX], BL
                TEST BL, BL
                JZ INC_COUNT
                INC ECX
                JMP COPY_RAND_LOOP
        TERMINATE_RAND:
                MOV BYTE PTR [EDI + 19], 0
        INC_COUNT:
                MOV EAX, count
                INC EAX
                MOV count, EAX
        NEXT_ITERATION:
                MOV EAX, i
                INC EAX
                MOV i, EAX
                JMP MAIN_LOOP
        END_MAIN:
                MOV EAX, num_obstacles
                MOV ECX, count
                MOV DWORD PTR [EAX], ECX
    }
}
SKIERDLL_API void updateObstacles(int score, int* added_trees, int* added_flags) {
    __asm {
        MOV EAX, score
        TEST EAX, EAX
        JLE CHECK_FLAGS
        XOR EDX, EDX
        MOV ECX, 150
        DIV ECX
        TEST EDX, EDX
        JNZ CHECK_FLAGS
        MOV EBX, added_trees
        MOV ECX, DWORD PTR [EBX]
        CMP ECX, 20
        JGE CHECK_FLAGS
        ADD ECX, 2
        MOV DWORD PTR [EBX], ECX
        CHECK_FLAGS:
            MOV EAX, score
            TEST EAX, EAX
            JLE END_UPDATE
            XOR EDX, EDX
            MOV ECX, 200
            DIV ECX
            TEST EDX, EDX
            JNZ END_UPDATE
            MOV EBX, added_flags
            MOV ECX, DWORD PTR [EBX]
            CMP ECX, 10
            JGE END_UPDATE
            INC ECX
            MOV DWORD PTR [EBX], ECX
        END_UPDATE:
    }
}
//Speed
SKIERDLL_API void updateSpeed(int score, int* speed_bonus, int* base_speed, const int* speed_levels, int levels_count, int* achieved_levels,
    int* achieved_count, int direction, int* current_speed) {
    int i, j, level, already_achieved;
    __asm {
        MOV i, 0

        OUTER_LOOP:
            MOV EAX, i
            CMP EAX, levels_count
            JGE CALC_CURRENT_SPEED
            MOV EBX, speed_levels
            MOV ECX, i
            IMUL ECX, 4
            ADD EBX, ECX
            MOV EDX, DWORD PTR [EBX]
            MOV level, EDX

            MOV EAX, score
            CMP EAX, level
            JL NEXT_OUTER

            MOV already_achieved, 0
            MOV j, 0
            
            INNER_LOOP:
                MOV EBX, achieved_count
                MOV ECX, DWORD PTR [EBX]
                MOV EAX, j
                CMP EAX, ECX
                JGE CHECK_ACHIEVED
                
                MOV EBX, achieved_levels
                MOV ECX, j
                IMUL ECX, 4
                ADD EBX, ECX
                MOV EDX, DWORD PTR [EBX]
                CMP EDX, level
                JNE NEXT_INNER

                MOV already_achieved, 1
                JMP CHECK_ACHIEVED

                NEXT_INNER:
                    INC j
                    JMP INNER_LOOP

            CHECK_ACHIEVED:
                CMP already_achieved, 0
                JNE NEXT_OUTER

                MOV EBX, achieved_count
                MOV ECX, DWORD PTR [EBX]
                MOV EDI, achieved_levels
                IMUL ECX, 4
                ADD EDI, ECX
                MOV EDX, level
                MOV DWORD PTR [EDI], EDX

                MOV EBX, achieved_count
                MOV ECX, DWORD PTR [EBX]
                INC ECX
                MOV DWORD PTR [EBX], ECX

                MOV EBX, speed_bonus
                MOV ECX, DWORD PTR [EBX]
                INC ECX
                MOV DWORD PTR [EBX], ECX

                MOV EBX, base_speed
                MOV ECX, DWORD PTR [EBX]
                INC ECX
                MOV DWORD PTR [EBX], ECX

                NEXT_OUTER:
                    INC i
                    JMP OUTER_LOOP

        CALC_CURRENT_SPEED:
            MOV EAX, direction
            MOV EBX, EAX
            SAR EBX, 31
            XOR EAX, EBX
            SUB EAX, EBX
            IMUL EAX, 2
            
            MOV EBX, base_speed
            MOV ECX, DWORD PTR [EBX]
            SUB ECX, EAX

            MOV EBX, current_speed
            MOV DWORD PTR [EBX], ECX
    }
}

//GameState
SKIERDLL_API GameState* GameState_create() {
    GameState* state;
    __asm {
        PUSH 28
        CALL malloc
        ADD ESP, 4
        MOV state, EAX

        TEST EAX, EAX
        JZ END_CREATE

        MOV DWORD PTR[EAX], 0
        MOV DWORD PTR[EAX + 4], 0
        MOV DWORD PTR[EAX + 8], 0
        MOV DWORD PTR[EAX + 12], 0
        MOV DWORD PTR[EAX + 16], 0
        MOV DWORD PTR[EAX + 20], 7
        MOV DWORD PTR[EAX + 24], 0

        END_CREATE:
    }
    return state;
}
SKIERDLL_API void GameState_updateDistance(GameState* state, int speed_y) {
    __asm {
        MOV EAX, state
        TEST EAX, EAX
        JZ END_UPDATE

        MOV ECX, speed_y
        ADD DWORD PTR [EAX], ECX

        END_UPDATE:
    }
}
SKIERDLL_API void GameState_addScore(GameState* state, int points) {
    __asm {
        MOV EAX, state
        TEST EAX, EAX
        JZ END_ADD

        MOV ECX, points
        ADD DWORD PTR [EAX + 4], ECX

        END_ADD:
    }
}
SKIERDLL_API int updateObstaclesCycle(GameState* state, int speed_y) {
    int needs_update;
    __asm {
        MOV EAX, state
        TEST EAX, EAX
        JNZ STATE_VALID

        MOV needs_update, 0
        JMP END_CYCLE

        STATE_VALID:
            MOV needs_update, 0
            MOV ECX, DWORD PTR [EAX]
            CMP ECX, 640
            JL CHECK_SECOND

            MOV EDX, DWORD PTR [EAX + 8]
            TEST EDX, EDX
            JNZ CHECK_SECOND

            MOV DWORD PTR [EAX + 8], 1
            MOV needs_update, 1

        CHECK_SECOND:
            MOV ECX, DWORD PTR [EAX]
            CMP ECX, 1280
            JL END_CYCLE

            MOV EDX, DWORD PTR [EAX + 8]
            CMP EDX, 1
            JNE END_CYCLE
            
            MOV DWORD PTR [EAX + 8], 0

            MOV ECX, DWORD PTR [EAX]
            SUB ECX, 1280
            MOV DWORD PTR [EAX], ECX
            MOV needs_update, 2

        END_CYCLE:
    }
    return needs_update;
}
SKIERDLL_API int checkCollision(int x1, int y1, int w1, int h1, int x2, int y2, int w2, int h2) {
    int overlapX, overlapY, result;
    __asm {
        MOV EAX, x2
        ADD EAX, w2
        MOV EBX, x1
        CMP EBX, EAX
        JGE NO_OVERLAP_X

        MOV EAX, x1
        ADD EAX, w1
        MOV EBX, x2
        CMP EAX, EBX
        JLE NO_OVERLAP_X

        MOV overlapX, 1
        JMP CHECK_Y

        NO_OVERLAP_X:
            MOV overlapX, 0

        CHECK_Y:
            MOV     EAX, y2
            ADD     EAX, h2
            MOV     EBX, y1
            CMP     EBX, EAX
            JGE     NO_OVERLAP_Y

            MOV     EAX, y1
            ADD     EAX, h1
            MOV     EBX, y2
            CMP     EAX, EBX
            JLE     NO_OVERLAP_Y

            MOV     overlapY, 1
            JMP     CHECK_RESULT

            NO_OVERLAP_Y:
                MOV overlapY, 0

        CHECK_RESULT:
            MOV EAX, overlapX
            TEST EAX, EAX
            JZ NO_COLLISION

            MOV EAX, overlapY
            TEST EAX, EAX
            JZ NO_COLLISION

            MOV result, 1
            JMP END_CHECK

        NO_COLLISION :
            MOV result, 0

        END_CHECK :
    }
    return result;
}
