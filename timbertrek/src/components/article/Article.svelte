<script lang="ts">
  import { onMount } from 'svelte';
  import TimberTrek from '../timber/Timber.svelte';
  import { fade, fly } from 'svelte/transition';

  let component: HTMLElement | null = null;
  let curDataset = 'my own set';
  let timbertrekTransitioning = false;

  const datasets = ['', '', '', 'my own set'];

  const optionClicked = (dataset: string) => {
    timbertrekTransitioning = true;
    curDataset = dataset;
  };

  onMount(() => {
    //pass
  });
</script>

<style lang="scss">
  @import './Article.scss';
</style>

<svelte:head>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link
    href="https://fonts.googleapis.com/css2?family=Lato&display=swap"
    rel="stylesheet"
  />
</svelte:head>

<div class="article-page">
  <div class="main-app" bind:this={component} tabindex="-1">
    <div class="timbertrek-app">
      {#key curDataset}
        <div
          class="timbertrek-wrapper"
          out:fly={{ x: -300, duration: 300 }}
          in:fly={{ x: 300, duration: 300 }}
          on:introstart={() => {
            timbertrekTransitioning = true;
          }}
          on:introend={() => {
            timbertrekTransitioning = false;
          }}
        >
          <TimberTrek
            notebookMode={false}
            {curDataset}
            {timbertrekTransitioning}
          />
        </div>
      {/key}
    </div>

    <div class="dataset-options">
      <span class="option-title"></span>
      <div class="options">
        {#each datasets as name, i}
          <span
            class="option"
            class:selected={name === curDataset}
            on:click={() => optionClicked(name)}
            data-text={name}
          >
            {name}
          </span>
        {/each}
      </div>
    </div>
  </div>
</div>
