import sys
import pygame
from time import sleep
from bullet import Bullet
from alien import Alien


def check_keydown_events(ai_settings, bullets, event, screen, ship):
    '''Respond to keypresses.'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, bullets, screen, ship)
    elif event.key == pygame.K_ESCAPE:
        sys.exit()

def check_keyup_events(event, ship):
    '''Respond to key releases.'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_play_button(ai_settings, aliens, bullets, mouse_x, mouse_y, play_button, sb, screen, ship, stats):
    '''Start a new game when the player click Play.'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings and statistics.
        ai_settings.initialize_dynamic_settings()
        stats.reset_stats()
        stats.game_active = True
        pygame.mouse.set_visible(False)

        # Reset the scoreboard images.
        sb.prep_high_score()
        sb.prep_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the lists of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, aliens, screen, ship)
        ship.center_ship()


def check_events(ai_settings, aliens, bullets, play_button, sb, screen, ship, stats):
    '''Respond to keypresses and mouse events.'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(ai_settings, bullets, event, screen, ship)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, aliens, bullets, mouse_x, mouse_y, play_button, sb, screen, ship, stats)


def update_screen(ai_settings, aliens, bullets, play_button, sb, screen, ship, stats):
    '''Update images on the screen and flip to the new screen.'''
    # Redraw the screen during each pass through the loop.
    #screen.fill(ai_settings.bg_color)
    screen.blit(ai_settings.bg, screen.get_rect())
    sb.show_score()
    ship.blitme()
    aliens.draw(screen)
    # Redraw all bullets behind the ship.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()

def update_bullets(ai_settings, aliens, bullets, sb, screen, ship, stats):
    '''Update position of bullets and get rid of old bullets.'''
    # Update bullets position.
    bullets.update()

    check_bullet_alien_collision(ai_settings, aliens, bullets, sb, screen, ship, stats)

    # Get rid of bullets that have dissapeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

def check_bullet_alien_collision(ai_settings, aliens, bullets, sb, screen, ship, stats):
    '''Respond to bullet-alien collisions.'''
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        stats.score += ai_settings.alien_points * len(collisions)
        sb.prep_score()

    if len(aliens) == 0:
        # Destroy existing bullets and create new fleet.
        bullets.empty()
        ai_settings.increase_speed()
        # Increase level.
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, aliens, screen, ship)

def fire_bullet(ai_settings, bullets, screen, ship):
    '''Fire a bullet if limit not reached yet.'''
    # Create new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
    '''Determine the number of aliens that fit in a row.'''
    available_space_x = ai_settings.screen_width - 2*alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, alien_height, ship):
    '''Determine the number of rows in alien fleet.'''
    available_space_y = ai_settings.screen_height - (3*alien_height) - ship.rect.width
    number_rows = int(available_space_y / (2*alien_height))
    return number_rows

def create_alien(ai_settings, aliens, alien_number, row_number, screen):
    # Create an alien and place it in the row.
    # Spacing between each alien is equal to one alien width.
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    alien.x = alien_width + 2*alien_width*alien_number
    alien.y = alien_height + 2*alien_height*row_number
    alien.rect.x = alien.x
    alien.rect.y = alien.y
    aliens.add(alien)

def create_fleet(ai_settings, aliens, screen, ship):
    '''Create a full fleet of aliens.'''
    # Create an alien and find the number of aliens in a row.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, alien.rect.height, ship)

    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, aliens, alien_number, row_number, screen)

def check_fleet_edges(ai_settings, aliens):
    '''Respond appropriately if any aliens have reached an edge.'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    '''Drop the entire fleet and change the fleet's direction.'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, aliens, bullets, sb, screen, ship, stats):
    '''Respond to ship hit by alien.'''
    if stats.ships_left > 1:
        # Decriment ships left.
        stats.ships_left -= 1
        sb.prep_ships()

        # Empty the lists of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, aliens, screen, ship)
        ship.center_ship()

        # Pause.
        sleep(1)

    else:
        check_high_score(sb, stats)
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, aliens, bullets, sb, screen, ship, stats):
    '''Check if any aliens have reached the bottom of the screen.'''
    for alien in aliens.sprites():
        if alien.rect.bottom >= ship.screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, aliens, bullets, sb, screen, ship, stats)
            break

def update_aliens(ai_settings, aliens, bullets, sb, screen, ship, stats):
    '''Check if the fleet is at an edge, and then update the positions of all alien in the fleet.'''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, aliens, bullets, sb, screen, ship, stats)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, aliens, bullets, sb, screen, ship, stats)

def check_high_score(sb, stats):
    '''Check to see is there's a new high score.'''
    if stats.high_score < stats.score:
        stats.high_score = stats.score
        sb.prep_high_score()
