import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ButtonModule } from 'primeng/button';
import { UserProfile } from './users/user-profile/user-profile';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, ButtonModule, UserProfile],
  templateUrl: './app.html',
  styleUrl: './app.css'

})
export class App {
  protected readonly title = signal('Fiware-web');

  



}
