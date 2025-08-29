import { Component, signal } from '@angular/core';
import { QuizComponent } from './quiz/quiz';
import { NavbarComponent } from './navbar/nav';
import { HomeComponent } from './home/home';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,              
  imports: [QuizComponent, NavbarComponent, CommonModule, HomeComponent, RouterOutlet],      
  templateUrl: './app.html',
  styleUrls: ['./app.css']       
})
export class App {
  protected readonly title = signal('quizapp');
}
