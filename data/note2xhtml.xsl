<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:tomboy="http://beatniksoftware.com/tomboy"
		xmlns:size="http://beatniksoftware.com/tomboy/size"
		xmlns:link="http://beatniksoftware.com/tomboy/link"
                version='1.0'>

<xsl:output method="html" indent="no" />
<xsl:preserve-space elements="*" />

<xsl:param name="base-user-url" />

<xsl:param name="newline" select="'&#xA;'" />

<xsl:template match="/">
	<xsl:apply-templates select="tomboy:note-content"/>
</xsl:template>

<xsl:template match="text()">
   <xsl:call-template name="softbreak"/>
</xsl:template>

<xsl:template name="softbreak">
	<xsl:param name="text" select="."/>
	<xsl:choose>
		<xsl:when test="contains($text, '&#x000a;')">
			<xsl:value-of select="substring-before($text, '&#x000a;')"/>
			<br/>
			<xsl:call-template name="softbreak">
				<xsl:with-param name="text" select="substring-after($text, '&#x000a;')"/>
			</xsl:call-template>
		</xsl:when>
		
		<xsl:otherwise>
			<xsl:value-of select="$text"/>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<xsl:template match="tomboy:note-content">
	<div>
		<xsl:apply-templates select="node()" />
	</div>
</xsl:template>

<xsl:template match="tomboy:bold">
	<b><xsl:apply-templates select="node()"/></b>
</xsl:template>

<xsl:template match="tomboy:italic">
	<i><xsl:apply-templates select="node()"/></i>
</xsl:template>

<xsl:template match="tomboy:strikethrough">
	<strike><xsl:apply-templates select="node()"/></strike>
</xsl:template>

<xsl:template match="tomboy:highlight">
	<span class="note-highlight"><xsl:apply-templates select="node()"/></span>
</xsl:template>

<xsl:template match="tomboy:datetime">
	<span class="note-datetime">
		<xsl:apply-templates select="node()"/>
	</span>
</xsl:template>

<xsl:template match="size:small">
	<span class="note-size-small"><xsl:apply-templates select="node()"/></span>
</xsl:template>

<xsl:template match="size:large">
	<span class="note-size-large"><xsl:apply-templates select="node()"/></span>
</xsl:template>

<xsl:template match="size:huge">
	<span class="note-size-huge"><xsl:apply-templates select="node()"/></span>
</xsl:template>

<xsl:template match="link:broken">
	<span class="link-broken">
		<xsl:value-of select="node()"/>
	</span>
</xsl:template>

<xsl:template match="link:internal">
	<xsl:choose>
		<xsl:when test="@id">
			<a href="{$base-user-url}{@id}" class="link-internal">
				<xsl:value-of select="node()"/>
			</a>
		</xsl:when>
		<xsl:otherwise>
			<span class="link-broken">
				<xsl:value-of select="node()"/>
			</span>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<xsl:template match="link:url">
	<a href="{node()}" class="link-url"><xsl:value-of select="node()"/></a>
</xsl:template>

<xsl:template match="tomboy:list">
	<ul>
		<xsl:apply-templates select="tomboy:list-item" />
	</ul>
</xsl:template>

<xsl:template match="tomboy:list-item">
	<li>
		<xsl:if test="normalize-space(text()) = '' and count(tomboy:list) = 1 and count(*) = 1">
			<xsl:attribute name="style">list-style-type: none</xsl:attribute>
		</xsl:if>
		<xsl:attribute name="dir">
			<xsl:value-of select="@dir"/>
		</xsl:attribute>
		<xsl:apply-templates select="node()" />
	</li>
</xsl:template>

<!-- Evolution.dll Plugin -->
<!--
<xsl:template match="link:evo-mail">
	<a href="{./@uri}">
		<img alt="Open Email Link" width="16" height="10" border="0">
			Inline Base64 encoded stock_mail.png =)
			<xsl:attribute name="src">data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAKCAYAAAC9vt6cAAAABmJLR0QA/wD/AP+gvaeTAAAACXBI WXMAAAsQAAALEAGtI711AAAAB3RJTUUH1QkeAjYaRAvZgAAAALxJREFUKM+NkjGKw1AMRN+GhRS/ 2xP4EHZr0E1UxFVuoiKdikCKfxMfwKdw+3t1gb/F4hASe50BgZjRDEII/jAAtWmaCnxSAy+oZlYj YrfMbAkB4GsJiAjcnfPpRNzvrCHnjIjQdd3De3geUFX8diMdj6tmVX3jD6+EquLXKz9p37waANC2 LRfPpJTIOdP3PXuoEVFLKdXMaills5+m6f8jbq26dcTvRXR3RIR5njcDRIRxHFe14cMHenukX9eX mbvfl0q9AAAAAElFTkSuQmCC</xsl:attribute>
		</img>
		<xsl:value-of select="node()"/>
	</a>
</xsl:template>
-->

<!-- FixedWidth.dll Plugin -->
<xsl:template match="tomboy:monospace">
	<span class="note-monospace"><xsl:apply-templates select="node()"/></span>
</xsl:template>

<!-- Bugzilla.dll Plugin -->
<!--
<xsl:template match="link:bugzilla">
	<a href="{@uri}"><xsl:value-of select="node()" /></a>
</xsl:template>
-->

</xsl:stylesheet>
