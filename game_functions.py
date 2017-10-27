import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    # create a bullet
    elif event.key == pygame.K_SPACE:
        # limit of condition
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
                 bullets):
    # check event of keyboard and mouse
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                              ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button,
                      ship, aliens, bullets, mouse_x, mouse_y):
    """begin game when player click 'play'"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # reset settings of game
        ai_settings.initialize_dynamic_settings()
        # hide cursor
        pygame.mouse.set_visible(False)
        # reset information
        stats.reset_stats()
        stats.game_active = True

        # reset scoreboard
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # clear list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # create new aliens and put ship in center
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens,  bullets,
                  play_button):
    # redraw screen every time
    screen.fill(ai_settings.bg_color)

    # draw every bullet
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    # draw button if game in inactive
    if not stats.game_active:
        play_button.draw_button()
    # make drew screen visible recently
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens,
                                  bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
        # check for collision
        collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
        if len(aliens) == 0:
            # delete existing bullets and create fleet
            bullets.empty()
            ai_settings.increase_speed()

            # improve level
            stats.level += 1
            sb.prep_level()
            create_fleet(ai_settings, screen, ship, aliens)

        if collisions:
            for aliens in collisions.values():
                stats.score += ai_settings.alien_points * len(aliens)
                sb.prep_score()
            check_high_score(stats, sb)


def fire_bullet(ai_settings, screen, ship, bullets):
    """ Only shot one bullet if at limit"""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def create_fleet(ai_settings, screen, ship, aliens):
    """create fleet"""
    # create a alien and
    # interval equal to width
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_aliens_x(ai_settings, alien_width):
    # count one row can hold how many aliens
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # create an alien then join in row
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    alien.rect.x = alien.x
    aliens.add(alien)


def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def update_aliens(ai_settings, screen, stats, sb, ship, aliens,
                  bullets):
    """update location of all alien"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # check for collision between aliens and ship
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
        print("ship hit!!!")

    # check whether aliens arrive at bottom
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_fleet_edges(ai_settings, aliens):
    """take some action when alien arrive at margin"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    # move down all aliens and change their direction
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):

    if stats.ships_left > 0:
        # ship_left minus 1
        stats.ships_left -= 1

        # update scoreboard
        sb.prep_ships()

        # clear list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # create new aliens and put ship in center
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # suspend
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """check whether alien arrive at bottom"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # deal like ship hit
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def check_high_score(stats, sb):
    """check whether there is the highest score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()













