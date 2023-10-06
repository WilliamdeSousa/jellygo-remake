from game.functions import *


class Selection:
    def __init__(self) -> None:
        self.selects: list = list()
        self.select_count = 0
        self.target = None
        self.TARGET_COLOR: color = TARGET_COLOR
        self.COLOR: color = SELECT_COLOR
        self.RADIUS = SELECT_RADIUS   
        self.WIDTH = SELECT_WIDTH
        self.initial_select: Coordinate = None

    def add_select(self, member) -> None:
        self.selects.append(member)
        self.select_count += 1
        member.select = True

    def add_selects(self, members: list) -> None:
        for member in members:
            self.add_select(member)
        
    def clear(self) -> None:
        for member in self.selects:
            member.select = False
        self.selects.clear()
        self.target = None
        self.select_count = 0
    
    def target_to(self, target) -> None:
        self.target = target
    
    def target_none(self) -> None:
        self.target = None

    def draw_circles(self) -> None:
        for select in self.selects:
            pg.draw.circle(screen, self.COLOR, select.position, self.RADIUS, self.WIDTH)
    
    def draw_lines(self) -> None:
        if self.target is None:
            target = pg.mouse.get_pos()
            lock = False
        else:
            target = self.target.position
            lock = True
        
        for select in self.selects:
            start, end = line_tangent(select.position, target, lock)
            pg.draw.line(screen, self.COLOR, start, end, SELECT_WIDTH)

    def get_rect(self) -> Rect:
        return rect_two_dots(self.initial_select, pg.mouse.get_pos())

    def draw_rect(self) -> None:
        if self.initial_select is not None:
            pg.draw.rect(screen, SELECT_COLOR, self.get_rect(), SELECT_WIDTH)

    def valid_target(self) -> None:
        return self.target is not None and (self.select_count == 1 and self.target != self.selects[0] or self.select_count > 1)

    def draw_target(self) -> None:
        if self.valid_target():
            pg.draw.circle(screen, TARGET_COLOR, self.target.position, SELECT_RADIUS, SELECT_WIDTH)

    def render(self) -> None:
        self.draw_circles()
        self.draw_lines()
        self.draw_target()


class Team:
    def __init__(self, color: color = PURPLE) -> None:
        self.members: list = list()
        self.color = color
        self.balls = []

    def add_member(self, member) -> None:
        self.members.append(member)


class Score(pg.font.Font):
    def __init__(self, name: None = None, size: int = 50) -> None:
        super().__init__(name, size)
        self.color: color = SCORE_COLOR
        self.points: float = 0.0
        self.growth_rate: float = 0.8
        self.max_points: float = 10.0
    
    def upgrade(self) -> None:
        pass
    
    def update(self) -> None:
        if self.points <= self.max_points:
            self.color = WHITE
            self.points += self.growth_rate * 0.025
        else:
            self.color = YELLOW
    
    def set_growth_rate(self, growth_rate: float) -> None:
        self.growth_rate = growth_rate

    def set_max_points(self, max_points: float) -> None:
        self.max_points = max_points

    def render(self, position: Coordinate) -> None:
        score = super().render(f'{int(self.points)}', 0, self.color)
        self.update()
        size = score.get_size()
        position = [position.x - (size[0] // 2), position.y - (size[1] // 2)]
        screen.blit(score, position)

    def attack(self, double: bool = False) -> int:
        if double:
            attack = int(self.points)
            self.points = 0
            return attack
        else:
            attack = self.points // 2
            self.points -= attack
            return attack


class Score_Ball(Score):
    def __init__(self, name: None = None, size: int = 10, attack: int = 0, position: Coordinate = None) -> None:
        super().__init__(name, size)
        self.position: Coordinate = Vector2(position)
        self.points: float = attack
    
    def update(self) -> None:
        pass


class Skill:
    def __init__(self, _class: str, level: int) -> None:
        self.level: int = level
        self.score: Score = Score()
        self.score.set_max_points(MAX_POINTS[level])


class Cell:
    def __init__(self, team: Team, level: int, _class: str, position: Coordinate) -> None:
        self.position: Coordinate = Vector2(position)
        self.skill: Skill = Skill(_class, level)
        self.score: Score = self.skill.score
        self.team: Team = team
        self.rect: Rect = None
        self.team.add_member(self)
    
    def get_rect(self) -> Rect:
        return self.rect

    def draw_body(self) -> None:
        self.rect = pg.draw.circle(screen, self.team.color, self.position, RADIUS_CELLS)

    def draw_score(self) -> None:
        self.score.render(self.position)
    
    def render(self) -> None:
        self.draw_body()
        self.draw_score()

    def attack(self, double: bool = False) -> None:
        attack = self.score.attack(double)
        self.team.balls.append(Ball(self, attack))


class Ball(Cell):
    def __init__(self, dad, attack) -> None:
        global game
        self.position: Coordinate = Vector2(dad.position)
        self.target: Cell = game.levels[game.level].selection.target
        self.rect: Rect = None
        self.speed: float = 1
        self.score: Score = Score_Ball(attack=attack, position=self.position)
    
    def update(self) -> None:
        self.position.move_towards_ip(self.target.position, self.speed * BALL_SPEED)


class Level:
    def __init__(self, teams, cells) -> None:
        self.teams = teams
        self.player_team = teams[0]
        self.cells = cells
        self.selection = Selection()
        self.bg_color = BG_COLOR
    
    def render_bg(self) -> None:
        screen.fill(self.bg_color)

    def render_cells(self) -> None:
        for cell in self.cells:
            cell.render()

    def render(self) -> None:
        self.render_bg()
        self.selection.render()
        self.render_cells()
        self.selection.draw_rect()


class Controls:
    def __init__(self, game) -> None:
        self.game = game
        self.level = self.game.levels[self.game.level]

    def select_all(self) -> None:
        self.level.selection.add_selects(self.game.teams[0].members)
    
    def mouse_up(self) -> None:
        selection = self.level.selection
        if not self.attack():    
            self.selection()    
        selection.initial_select = None
    
    def selection(self) -> None:
        selection = self.level.selection
        select_rect = selection.get_rect()
        selects = []
        for cell in self.level.player_team.members:
            if is_select(cell, select_rect):
                selects.append(cell)
        selection.clear()
        selection.add_selects(selects)

    def mouse_down(self) -> None:
        self.level.selection.initial_select = pg.mouse.get_pos()
    
    def attack(self) -> bool:
        selection = self.level.selection
        if selection.valid_target():
            for cell in selection.selects:
                cell.attack(selection.target)
            selection.clear()
            return True
        return False


class Game:
    def __init__(self) -> None:
        self.teams = [Team(BLUE), Team(RED)]
        self.levels = [
            Level(
                teams=self.teams, 
                cells=[
                    Cell(self.teams[0], 3, 'd', [500, 275]),
                    Cell(self.teams[0], 1, 'd', [500, 425]),
                    Cell(self.teams[1], 2, 'd', [800, 350])
                    ]
                )
            ]
        self.level = 0
        self.control = Controls(self)

    def run(self) -> None:
        self.check_targets()
        self.levels[self.level].render()
        pg.display.flip()
        clock.tick(60)
    
    def check_targets(self) -> None:
        for cell in self.levels[self.level].cells:
            if mouse_colide(cell):
                self.levels[self.level].selection.target_to(cell)
                break
        else:
            self.levels[self.level].selection.target_none()


game = Game()