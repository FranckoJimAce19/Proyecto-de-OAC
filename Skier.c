#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int centerx;
    int centery;
} Rect;

typedef struct {
    int direction;
    char **imagpaths;
    Rect rect;
    int speed[2];
    // In C, image loading and handling would require a graphics library.
    // Here we just store the image path as a placeholder.
    char *image_path;
} SkierClass;

void load_image(SkierClass *skier, const char *path) {
    // Placeholder for image loading
    skier->image_path = (char *)path;
}

void init_skier(SkierClass *skier, char **image_paths, int image_count) {
    skier->direction = 0;
    skier->imagpaths = image_paths;
    load_image(skier, skier->imagpaths[skier->direction]);
    skier->rect.centerx = 320;
    skier->rect.centery = 100;
    skier->speed[0] = skier->direction;
    skier->speed[1] = 6 - abs(skier->direction) * 2;
}

void turn(SkierClass *skier, int num) {
    skier->direction += num;
    if (skier->direction < -2) skier->direction = -2;
    if (skier->direction > 2) skier->direction = 2;
    int centerx = skier->rect.centerx;
    int centery = skier->rect.centery;
    load_image(skier, skier->imagpaths[skier->direction]);
    skier->rect.centerx = centerx;
    skier->rect.centery = centery;
    skier->speed[0] = skier->direction;
    skier->speed[1] = 6 - abs(skier->direction) * 2;
}

void move(SkierClass *skier) {
    skier->rect.centerx += skier->speed[0];
    if (skier->rect.centerx < 20) skier->rect.centerx = 20;
    if (skier->rect.centerx > 620) skier->rect.centerx = 620;
}

void setFall(SkierClass *skier, const char *fall_image_path) {
    load_image(skier, fall_image_path);
}

void setForward(SkierClass *skier) {
    skier->direction = 0;
    load_image(skier, skier->imagpaths[skier->direction]);
}