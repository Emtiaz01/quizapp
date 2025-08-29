import { Routes } from '@angular/router';
import { HomeComponent } from './home/home';
import { QuizComponent } from './quiz/quiz';

export const routes: Routes = [
  { path: '', component: HomeComponent },   
  { path: 'quiz', component: QuizComponent },
  { path: '**', redirectTo: '' }            
];
