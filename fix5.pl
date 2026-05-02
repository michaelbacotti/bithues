#!/usr/bin/env perl
use strict;
use File::Basename;

my $dir = '/Users/mike/.openclaw/workspace-bacottibot/websites/bithues/Website/bithues/stories';
my @files = glob "$dir/*.html";

my $fixed = 0;
my @reports;

my $nav_block = <<'NAV';
  <nav>
    <a href="../index.html" class="nav-brand">Bithues <span>Reading Lab</span></a>
    <div class="nav-links">
      <div class="nav-item"><a href="../index.html" class="active">Home</a></div>
      <div class="nav-item">
        <a href="../catalog.html">Reviews ▾</a>
        <div class="dropdown">
          <a href="../catalog.html">All Reviews</a>
          <a href="../category/self-help.html">Self-Help</a>
          <a href="../category/science-fiction.html">Sci-Fi</a>
          <a href="../category/fantasy.html">Fantasy</a>
          <a href="../category/nonfiction.html">Nonfiction</a>
          <a href="../category/thriller.html">Thriller</a>
          <a href="../category/biography.html">Biography</a>
          <a href="../category/business.html">Business</a>
        </div>
      </div>
      <div class="nav-item">
        <a href="../stories.html">Stories ▾</a>
        <div class="dropdown">
          <a href="../stories.html">All Stories</a>
        </div>
      </div>
      <div class="nav-item">
        <a href="../articles.html">Articles ▾</a>
        <div class="dropdown">
          <a href="../articles.html">All Articles</a>
          <a href="../articles/dna-ancestry-historical-fiction.html">DNA &amp; Historical Fiction</a>
        </div>
      </div>
      <div class="nav-item"><a href="../about.html">About</a></div>
      <div class="nav-item"><a href="../contact.html">Contact</a></div>
    </div>
  </nav>
NAV

chomp($nav_block);

for my $filepath (@files) {
  my $filename = basename($filepath);
  local $/;

  open(my $fh, '<', $filepath) or die "Cannot read $filepath: $!";
  my $content = <$fh>;
  close($fh);

  my $original = $content;
  my @changes;

  # Fix 1: If no nav tag exists but body exists, inject nav before <section class="hero">
  if ($content !~ /<nav>/ && $content =~ /<section class="hero">/) {
    $content =~ s{<section class="hero">}{$nav_block\n\n  <section class="hero">};
    push @changes, "nav-injected";
  }

  # Fix 2: If nav exists but Home link is malformed, fix it
  if ($content =~ s{<div class="nav-item"><a href="\.\./index\.html">Home\s*</div>}{<div class="nav-item"><a href="../index.html" class="active">Home</a></div>}g) {
    push @changes, "home-nav-fixed";
  }

  # Fix 3: Fix any remaining malformed article tags
  if ($content =~ s{<article<!-- ── CATEGORIES ── -->>}{<article>}g) {
    push @changes, "article-tag-fixed";
  }

  # Fix 4: Fix chips links - add ../ prefix to category hrefs that don't have it
  # These should be ../category/xxx since we're in stories/
  if ($content =~ s{href="category/(fiction|self-help|science-fiction|fantasy|nonfiction|thriller|biography|business)\.html"}{href="../category/$1.html"}g) {
    push @changes, "chips-links-fixed";
  }

  # Fix 5: Remove extra </div> that appears between </article> and FOOTER comment
  if ($content =~ s{</article>\s*\n\s*</div>\s*\n\s*(<!-- ── FOOTER ── -->)}{</article>\n\n  $1}g) {
    push @changes, "orphan-div-removed";
  }

  if ($content ne $original) {
    open(my $fh, '>', $filepath) or die "Cannot write $filepath: $!";
    print $fh $content;
    close($fh);
    $fixed++;
    push @reports, "$filename: " . join(', ', @changes);
  }
}

print "=== ALL FIXES APPLIED ===\n";
print "Files modified: $fixed / 36\n\n";
for my $r (@reports) {
  print "$r\n";
}