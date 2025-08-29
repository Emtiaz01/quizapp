import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './home.html',
  styleUrls: ['./home.css']
})
export class HomeComponent {
  isStarted = false;
  selectedOption: string | null = null;
  singleVideoLink: string = '';
  multipleVideoLinks: string = '';
  pdfLink: string = '';

  start() {
    this.isStarted = true;
  }
  goBack() {
    this.isStarted = false;
    this.selectedOption = null;
    this.singleVideoLink = '';
    this.multipleVideoLinks = '';
    this.pdfLink = '';
  }

  selectOption(option: string) {
    this.selectedOption = option;
  }

  submitLink() {
    if (this.selectedOption === 'single') {
      console.log('Single Video Link:', this.singleVideoLink);
      // Backend integration...
    } else if (this.selectedOption === 'multiple') {
      console.log('Multiple Video Links:', this.multipleVideoLinks);
      // Backend integration...
    } else if (this.selectedOption === 'pdf') {
      console.log('PDF Link:', this.pdfLink);
      // Backend integration...
    }
  }
}
