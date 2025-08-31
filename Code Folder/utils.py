import math

def check_ball_collision(ball1, ball2):
    dx = ball2.x - ball1.x
    dy = ball2.y - ball1.y
    distance = math.hypot(dx, dy)
    if distance < ball1.radius + ball2.radius:
        # Elastic collision (swap velocities)
        ball1.dx, ball2.dx = ball2.dx, ball1.dx
        ball1.dy, ball2.dy = ball2.dy, ball1.dy
        return True
    return False
