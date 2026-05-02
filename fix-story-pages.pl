#!/usr/bin/env perl
use strict;
use File::Basename;

my $dir = '/Users/mike/.openclaw/workspace-bacottibot/websites/bithues/Website/bithues/stories';
my @files = glob "$dir/*.html";

my $fixed = 0;
my @reports;

for my $filepath (@files) {
  my $filename = basename($filepath);
  local $/; # slurp mode

  open(my $fh, '<', $filepath) or die "Cannot read $filepath: $!";
  my $content = <$fh>;
  close($fh);

  my $original = $content;
  my @changes;

  # 1. Fix missing </a> on Home nav link
  if ($content =~ s{<div class="nav-item"><a href="../index\.html">Home\s*</div>}{<div class="nav-item"><a href="../index.html" class="active">Home</a></div>}g) {
    push @changes, "home-closing-tag";
  }

  # 2. Remove breadcrumb div and all nav/hero content before <section class="hero">
  # Match from breadcrumb div through the HERO comment and hero section opening
  if ($content =~ s{<div class="breadcrumb"[^>]*>.*?<!-- ── NAV ── -->.*?<!-- ── HERO ── -->\s*<section class="hero">}{<section class="hero">}sg) {
    push @changes, "breadcrumb-nav-hero-cleanup";
  }

  # 3. Fix malformed <article<!-- ── CATEGORIES ── -->> (extra chevron and comment)
  if ($content =~ s{<article<!-- ── CATEGORIES ── -->>}{<article>}g) {
    push @changes, "article-malformed-tag";
  }

  # 4. Remove the three trailing </div> tags after </article>
  if ($content =~ s{(\s*</div>\s*){3}(\s*<!-- ── FOOTER ── -->)}{$1$2}gs) {
    push @changes, "trailing-divs";
  }

  if ($content ne $original) {
    open(my $fh, '>', $filepath) or die "Cannot write $filepath: $!";
    print $fh $content;
    close($fh);
    $fixed++;
    push @reports, "$filename: " . join(', ', @changes);
  }
}

print "=== FIXES APPLIED ===\n";
print "Files modified: $fixed / 36\n\n";
for my $r (@reports) {
  print "$r\n";
}