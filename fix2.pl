#!/usr/bin/env perl
use strict;
use File::Basename;

my $dir = '/Users/mike/.openclaw/workspace-bacottibot/websites/bithues/Website/bithues/stories';
my @files = glob "$dir/*.html";

my $fixed = 0;
my @reports;

for my $filepath (@files) {
  my $filename = basename($filepath);
  local $/;

  open(my $fh, '<', $filepath) or die "Cannot read $filepath: $!";
  my $content = <$fh>;
  close($fh);

  my $original = $content;
  my @changes;

  # Fix 1: Remove extra </div></div> after </article> (before story-footer or footer)
  # Pattern: </article> followed by whitespace then </div></div> then story-footer
  if ($content =~ s{</article>\s*</div>\s*</div>\s*\n\s*<div class="story-footer">}{</article>\n\n            <div class="story-footer">}g) {
    push @changes, "article-trailing-divs";
  }

  # Fix 2: Fix extra </div></div> after book-promo block (before story-footer div)
  # Pattern: book-promo closing </div> followed by extra </div></div> then story-footer
  if ($content =~ s{(class="book-promo">.*?</div>)\s*</div>\s*</div>\s*\n\s*<div class="story-footer">}{$1\n            <div class="story-footer">}gs) {
    push @changes, "book-promo-extra-divs";
  }

  # Fix 3: Ensure story-footer div has proper spacing after book-promo (both open/close)
  # For cases where story-footer is directly after book-promo without extra divs
  # Pattern: </article> </div> <div class="story-footer">
  if ($content =~ s{</article>\s*</div>\s*\n\s*<div class="story-footer">}{</article>\n\n            <div class="story-footer">}g) {
    push @changes, "article-story-footer-cleanup";
  }

  if ($content ne $original) {
    open(my $fh, '>', $filepath) or die "Cannot write $filepath: $!";
    print $fh $content;
    close($fh);
    $fixed++;
    push @reports, "$filename: " . join(', ', @changes);
  }
}

print "=== SECOND PASS FIXES ===\n";
print "Files modified: $fixed\n\n";
for my $r (@reports) {
  print "$r\n";
}